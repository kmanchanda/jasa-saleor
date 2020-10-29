from collections import defaultdict

from django.db.models import F

from ...order.models import Order, OrderLine
from ..core.dataloaders import DataLoader


class OrderLinesByVariantIdAndChannelIdLoader(DataLoader):
    context_key = "orderline_by_variant_and_channel"

    def batch_load(self, keys):
        channel_ids = [key[1] for key in keys]
        variant_ids = [key[0] for key in keys]
        order_lines = OrderLine.objects.filter(
            order__channel_id__in=channel_ids, variant_id__in=variant_ids
        ).annotate(channel_id=F("order__channel_id"))

        order_line_by_variant_and_channel_map = defaultdict(list)
        for order_line in order_lines:
            key = (order_line.variant_id, order_line.channel_id)
            order_line_by_variant_and_channel_map[key].append(order_line)
        return [order_line_by_variant_and_channel_map[key] for key in keys]


class OrderByIdLoader(DataLoader):
    context_key = "order_by_id"

    def batch_load(self, keys):
        orders = Order.objects.in_bulk(keys)
        return [orders.get(order_id) for order_id in keys]