# Generated by Django 3.2.19 on 2023-06-15 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('ID', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('Type', models.CharField(db_column='Type', max_length=250)),
                ('SKU', models.CharField(db_column='SKU', max_length=250)),
                ('Name', models.CharField(db_column='Name', max_length=250)),
                ('Published', models.BigIntegerField(db_column='Published')),
                ('Is_featured', models.BigIntegerField(db_column='Is featured?')),
                ('Visibility_in_catalog', models.CharField(db_column='Visibility in catalog', max_length=250)),
                ('Short_description', models.CharField(db_column='Short description', max_length=250)),
                ('description', models.TextField(verbose_name=models.TextField(db_column='description'))),
                ('Date_sale_price_starts', models.FloatField(db_column='Date sale price starts')),
                ('Date_sale_price_ends', models.FloatField(db_column='Date sale price ends')),
                ('Tax_status', models.FloatField(db_column='Tax status')),
                ('Tax_class', models.FloatField(db_column='Tax class')),
                ('In_stock', models.BigIntegerField(db_column='In stock?')),
                ('Stock', models.BigIntegerField(db_column='Stock')),
                ('Backorders_allowed', models.BigIntegerField(db_column='Backorders allowed?')),
                ('Sold_individually', models.BigIntegerField(db_column='Sold individually?')),
                ('Weight', models.FloatField(db_column='Weight (lbs)')),
                ('Length', models.FloatField(db_column='Length (in)')),
                ('Width', models.FloatField(db_column='Width (in)')),
                ('Height', models.FloatField(db_column='Height (in)')),
                ('Allow_customer_reviews', models.BigIntegerField(db_column='Allow customer reviews?')),
                ('Purchase_note', models.FloatField(db_column='Purchase note')),
                ('Sale_price', models.FloatField(db_column='Sale price')),
                ('Regular_price', models.FloatField(db_column='Regular price')),
                ('Categories', models.CharField(db_column='Categories', max_length=250)),
                ('Tags', models.FloatField(db_column='Tags')),
                ('Shipping_class', models.FloatField(db_column='Shipping class')),
                ('Images', models.CharField(db_column='Images', max_length=250)),
                ('Download_limit', models.FloatField(db_column='Download limit')),
                ('Download_expiry_days', models.FloatField(db_column='Download expiry days')),
                ('Parent', models.CharField(db_column='Parent', max_length=250)),
                ('Grouped_products', models.FloatField(db_column='Grouped products')),
                ('Upsells', models.FloatField(db_column='Upsells')),
                ('Cross_sells', models.FloatField(db_column='Cross-sells')),
                ('External_URL', models.FloatField(db_column='External URL')),
                ('Button_text', models.FloatField(db_column='Button text')),
                ('Position', models.FloatField(db_column='Position')),
                ('Attribute_1_name', models.CharField(db_column='Attribute 1 name', max_length=250)),
                ('Attribute_1_value', models.CharField(db_column='Attribute 1 value(s)', max_length=250)),
                ('Attribute_2_name', models.CharField(db_column='Attribute 2 name', max_length=250)),
                ('Attribute_2_value', models.CharField(db_column='Attribute 2 value(s)', max_length=250)),
                ('Attribute_3_name', models.CharField(db_column='Attribute 3 name', max_length=250)),
                ('Attribute_3_value', models.CharField(db_column='Attribute 3 value(s)', max_length=250)),
                ('Attribute_4_name', models.CharField(db_column='Attribute 4 name', max_length=250)),
                ('Attribute_4_value', models.CharField(db_column='Attribute 4 value(s)', max_length=250)),
                ('Attribute_5_name', models.CharField(db_column='Attribute 5 name', max_length=250)),
                ('Attribute_5_value', models.CharField(db_column='Attribute 5 value(s)', max_length=250)),
                ('Meta_wpcom_is_markdown', models.FloatField(db_column='Meta: _wpcom_is_markdown')),
                ('Download_1_name', models.FloatField(db_column='Download 1 name')),
                ('Download_1_URL', models.FloatField(db_column='Download 1 URL')),
                ('Download_2_name', models.FloatField(db_column='Download 2 name')),
                ('Download_2_URL', models.FloatField(db_column='Download 2 URL')),
            ],
            options={
                'db_table': 'Products',
            },
        ),
    ]