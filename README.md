# FeatFilter
WIP

##Quickstart:
* Clone repository or download source
* Install requirements\
<code>
$ pip install -r requirements.txt
</code>
* Init DB\
<code>
$ python manage.py migrate
</code>
 * Fill DB\
 <code>
 $ cd utils
 </code>\
 <code>
 $ python feat_parser.py
 </code>
 * Start server\
 <code>
 $ python manage.py runserver
 </code>