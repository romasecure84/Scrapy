# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['name'] = adapter['name'].upper()
        available_no = adapter.get('availability').split('(')[-1].split()[0]
        adapter['availability'] = available_no
        adapter['price_excl_tax'] = adapter.get('price_excl_tax').replace('£','$')
        adapter['price_incl_tax'] = adapter.get('price_incl_tax').replace('£', '$')
        adapter['tax'] = adapter.get('tax').replace('£', '$')
        return item
