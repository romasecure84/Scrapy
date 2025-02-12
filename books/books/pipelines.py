# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import openpyxl


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

class DropperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        available_no = adapter.get('availability').split('(')[-1].split()[0]
        if int(available_no) > 10:
            adapter['availability'] = available_no
            adapter['price_excl_tax'] = adapter.get('price_excl_tax').replace('£', '$')
            adapter['price_incl_tax'] = adapter.get('price_incl_tax').replace('£', '$')
            adapter['tax'] = adapter.get('tax').replace('£', '$')
            adapter['name'] = adapter['name'].upper()

            return item
        else:
            raise DropItem(f'{adapter['name']} not enough stock')

class ExcelPipeline:
    def open_spider(self, spider):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = 'Books'
        self.sheet.append(['name',
                           'price_excl_tax',
                           'price_incl_tax',
                           'category', 'stars',
                           'upc',
                           'tax',
                           'availability',
                           'image_url'])

    def process_item(self, item, spider):
        self.sheet.append([item.get('name'),
                           item.get('price_excl_tax'),
                           item.get('price_incl_tax'),
                           item.get('category'),
                           item.get('stars'),
                           item.get('upc'),
                           item.get('tax'),
                           item.get('availability'),
                           item.get('image_url')])
        return item

    def close_spider(self, spider):
        self.workbook.save('excelpipelines.xlsx')