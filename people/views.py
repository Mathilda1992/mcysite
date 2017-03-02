from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb
from people.models import Blog



from django.db.models import Q
from people.models import Book


from people.forms import ContactForm



# Create your views here.
def blog_list(request):
    db = MySQLdb.connect(user='root',db='mcysite_test',passwd='682101mcy',host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM people_blog')

    # title_list = cursor.fetchall()
    # for title in title_list:
    #     print title
    # return render_to_response('test.html',{'titleList':title_list})

    blogs = cursor.fetchall()
    for blog in blogs:
        print blog[1]# the return data is a tuple format
    db.close()
    return render_to_response('test.html',{'blogList':blogs})


def blog_list2(request):
    # blogs = Blog.objects.order_by('pub_date')
    blogs = Blog.objects.all()[0:2]
    return render_to_response('test.html',{'blogList':blogs})



#/*************************learn how to use form**********************************/
def search(request):
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(title_icontains=query)|
            Q(authors_first_name_icontains=query)|
            Q(authors_last_name_icontains=query)
        )
        results=Book.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('search.html',{"results":results,"query":query})



def contact(request):
    # form = ContactForm(initial={'sender':'user@example.com'})
    if request.method == 'POST':
        form =ContactForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/login/")
    else:
        form = ContactForm()
    return render_to_response('contact.html', {'form': form})



