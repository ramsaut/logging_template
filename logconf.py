import logging.config
import ecs_logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "human": {
            "format": "%(asctime)s - %(name)s:%(funcName)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
            "class": "logging.Formatter",
        },
        "ecs": {
            "class": "ecs_logging.StdlibFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "human",
        },
        "ecs_handler": {
            "class": "logging.FileHandler",
            "filename": "filebeat_ingest_data/main.json.log",
            "formatter": "ecs",
        },
    },
    "loggers": {"": {"handlers": ["stdout", "ecs_handler"], "level": "DEBUG"}},
}

def pkt2dict(pkt):
    packet_dict = {}
    for line in pkt.show2(dump=True).split('\n'):
        if '###' in line:
            if '|###' in line:
                sublayer = line.strip('|#[] ')
                packet_dict[layer][sublayer] = {}
            else:
                layer = line.strip('#[] ')
                packet_dict[layer] = {}
        elif '=' in line:
            if '|' in line and 'sublayer' in locals():
                key, val = line.strip('| ').split('=', 1)
                packet_dict[layer][sublayer][key.strip()] = val.strip('\' ')
            else: 
                key, val = line.split('=', 1)
                val = val.strip('\' ')
                if(val):
                    try:
                        packet_dict[layer][key.strip()] = eval(val)
                    except:
                        packet_dict[layer][key.strip()] = val
        else:
            logging.debug("pkt2dict packet not decoded: " + line)
    return packet_dict

def init():
    logging.config.dictConfig(LOGGING)