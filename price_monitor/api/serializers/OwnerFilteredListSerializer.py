from rest_framework import serializers


class OwnerFilteredListSerializer(serializers.ListSerializer):
    """
    Explicite list serializer class for lists, that need to be filtered by the owner attribute
    """

    def to_representation(self, data):
        """
        Filters the data to represent
        :param data: Subscription queryset
        :type data:  QuerySet
        :return:     list of child representations
        :rtype:      list
        """
        data = data.filter(owner=self.context['request'].user)
        return super(OwnerFilteredListSerializer, self).to_representation(data)
