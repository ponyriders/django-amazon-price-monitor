import logging

from celery.task import Task


logger = logging.getLogger('price_monitor')


class SynchronizeSingleProductTask(Task):
    """
    Task for synchronizing a single product.
    """

    def run(self, item_id):
        """
        Called by celery if task is being delayed.
        :param item_id: the ItemId that uniquely identifies a product
        :type  item_id: basestring
        """
        logger.info('synchronizing Product with ItemId %(item_id)s' % {'item_id': item_id})

        # TODO write some code ;-)
