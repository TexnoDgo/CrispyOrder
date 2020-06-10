from django.test import TestCase

# Create your tests here.
file = 'pdf/111.PDF'
print(file)
png_file = '{}{}'.format(file[4:-3], 'png')
print(png_file)