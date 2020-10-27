import can
import mongodb_can_writer

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
printer = can.Printer()
mongo_db_writer = mongodb_can_writer.mongodb_can_writer()
notifier = can.Notifier(bus, [printer, mongo_db_writer], timeout=1.0, loop=None)

