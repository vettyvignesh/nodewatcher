import datetime
import time

import datastream

from nodewatcher.utils import toposort

# Number of datapoints to commit in one batch.
COMMIT_BATCH_SIZE = 1000
# Number of bytes to commit in one batch.
COMMIT_BATCH_BYTE_SIZE = 5242880


def datastream_copy(source, destination, start=None, end=None, remove_all=False):
    """
    Copies all streams from one datastream backend to another. Source and destination
    MUST differ. All data in destination datastream backend WILL BE LOST.

    :param source: Source datastream backend instance
    :param destination: Destination datastream backend instance
    :param start: Import from the specified timestamp
    :param end: Import until the specified timestamp
    :param remove_all: Remove all destination streams
    """

    # Do a basic check if source and destination are the same. This cannot determine
    # if they are actually different in which case the copy will fail and all source
    # data will be lost.
    if source == destination:
        raise ValueError('Source and destination must differ!')

    if start is None:
        start = datetime.datetime.min

    ds_source = datastream.Datastream(source)
    ds_destination = datastream.Datastream(destination)

    # Load all stream metadata into memory.
    print "Loading streams from source."
    streams = {}
    for stream in ds_source.find_streams():
        streams[stream['stream_id']] = {
            'stream': stream,
            'dependencies': stream.get('derived_from', {}).get('stream_ids', []),
        }

    # Topologically sort the streams based on dependencies.
    print "Resolving dependencies with %d streams." % len(streams)
    sorted_streams = toposort.topological_sort(streams)

    if remove_all:
        print "Dropping destination streams."
        ds_destination.delete_streams()

    print "Importing streams."
    stream_no = 1
    stream_map = {}
    for stream_batch in sorted_streams:
        for stream in stream_batch:
            print "[%d/%d] Importing stream." % (stream_no, len(streams))

            stream = datastream.Stream(stream['stream'])
            value_downsamplers = list(set(stream.value_downsamplers).intersection(ds_destination.backend.value_downsamplers))

            # Create the same stream on the destination.
            kwargs = {}
            if hasattr(stream, 'derived_from'):
                # Resolve source streams.
                kwargs['derive_from'] = [{'stream': stream_map[derived_id]} for derived_id in stream.derived_from['stream_ids']]
                kwargs['derive_op'] = stream.derived_from['op']
                kwargs['derive_args'] = stream.derived_from['args']

                if stream.derived_from['op'] == 'counter_derivative':
                    kwargs['derive_from'][0]['name'] = 'reset'

            stream_id = ds_destination.ensure_stream(
                query_tags={'import_id': stream.id},
                tags=stream.tags,
                value_downsamplers=value_downsamplers,
                highest_granularity=stream.highest_granularity,
                value_type=stream.value_type,
                value_type_options=stream.value_type_options,
                **kwargs
            )

            stream_map[stream.id] = stream_id

            if not hasattr(stream, 'derived_from'):
                # Copy data.
                print "Copying data."
                batch = []
                size_of_batch = 0

                try:
                    def append_current_batch():
                        for i in xrange(10):
                            try:
                                ds_destination.append_multiple(batch)
                                break
                            except datastream.exceptions.StreamAppendFailed:
                                print "WARNING: Destination stream append failed. Retry #%d after 30 seconds." % (i + 1)
                                time.sleep(30)

                    for datapoint in ds_source.get_data(stream.id, stream.highest_granularity, start=start, end=end):
                        batch.append({'stream_id': stream_id, 'value': datapoint['v'], 'timestamp': datapoint['t']})
                        size_of_batch += len(str(datapoint['v']))
                        if len(batch) >= COMMIT_BATCH_SIZE or size_of_batch >= COMMIT_BATCH_BYTE_SIZE:
                            append_current_batch()
                            batch = []
                            size_of_batch = 0

                    if batch:
                        append_current_batch()
                        batch = []
                except datastream.exceptions.StreamNotFound:
                    # Stream has been removed while import was in progress. Remove the stream from
                    # destination as well.
                    print "Skipping removed stream."

                    try:
                        ds_destination.delete_streams({'import_id': stream.id})
                    except:
                        # Do not abort import when a stream cannot be deleted.
                        pass
                except:
                    print "ERROR: Failed to copy data for source stream %s (target %s)." % (stream.id, stream_id)
                    print "ERROR: Last batch was (%d items, %d bytes):" % (len(batch), size_of_batch)
                    for value in batch:
                        print "  %s" % repr(value['value'])
                    print "ERROR: Aborting due to exception."
                    raise

            stream_no += 1

    print "Backprocessing streams."
    ds_destination.backprocess_streams()

    print "Imported %d/%d streams." % (len(ds_destination.find_streams()), stream_no - 1)
