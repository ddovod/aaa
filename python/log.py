
import logging


log = logging.getLogger(__name__)
logging.basicConfig(filename='log.txt',
                    encoding='utf-8',
                    format='%(asctime)s | %(levelname)s :\t%(message)s',
                    level=logging.INFO)
