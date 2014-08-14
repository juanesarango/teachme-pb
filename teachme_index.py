from google.appengine.api import search
import teachme_db
import datetime

_INDEX_NAME = 'Profesores'

def list2string(listvar):
	stringvar=""
	for l in listvar:
		stringvar=stringvar+l+" "
	return stringvar

def create_index():
	index = search.Index(name=_INDEX_NAME)

	for i in teachme_db.teacher.query():
		
		fields = [
		    search.TextField(name="Nombre", value=i.name+" "+i.lname),
		    search.TextField(name="Ciudad", value=i.ciudad),
		    search.TextField(name="Pais", value=i.pais),
		    search.TextField(name="Idiomas", value=list2string(i.idiomas)),
		    search.TextField(name="Tags", value=list2string(i.tags)),
		    search.TextField(name="ID", value=str(i.key.id())),
		    search.DateField(name="Updated", value=datetime.datetime.now().date()),
		    
		    search.NumberField(name="Fee", value=i.fee),
		    search.NumberField(name="Rating", value=i.rating),
		    ]

		d = search.Document(doc_id = str(i.key.id()), fields=fields)

		try:
			index.put(d)
			print 'Indice creado'
		except:
			print 'No se pudo crear el indice'

def make_query(query_string, doc_limit=5):

	#ejemplo de un query_string: query_string = "Juan Esteban"
	try:
		index = search.Index(_INDEX_NAME)
		search_query = search.Query(
	    	query_string=query_string,
	    	options=search.QueryOptions(
          		limit=doc_limit))
  		search_results = index.search(search_query)
  		number_found = search_results.number_found
  		if number_found ==1:
  			print 'Se encontro ' +  str(number_found) + ' resultado'	
  		print 'Se encontraron ' +  str(number_found) + ' resultados'
		for document in search_results:
			print u"Document_id: {doc_id}\n".format(doc_id=document.doc_id)
			for f in document.fields:
				print u"{nombre_campo}: {valor_campo}\n".format(nombre_campo=f.name,valor_campo=f.value)
	except search.Error:
		print 'No se encontraron resultados'

def edit_index(id, field_name, field_value):
	index = search.Index(name=_INDEX_NAME)
	i = ndb.Key(urlsafe = str(id)).get()
	if field_name=="Nombre":
		v.nombre=field_value
	else:
		v.nombre=i.name+" "+i.lname
	if field_name=="Ciudad":
		v.ciudad=field_value
	else:
		v.ciudad=i.ciudad
	if field_name=="Pais":
		v.pais=field_value
	else:
		v.pais=i.pais
	if field_name=="Idiomas":
		v.idiomas=field_value
	else:
		v.idiomas=list2string(i.idiomas)
	if field_name=="Tags":
		v.tags=field_value
	else:
		v.tags=list2string(i.tags)
	if field_name=="Fee":
		v.fee=field_value
	else:
		v.fee=i.fee
	if field_name=="Rating":
		v.rating=field_value
	else:
		v.rating=i.rating
	
	fields = [
		    search.TextField(name="Nombre", value=v.nombre),
		    search.TextField(name="Ciudad", value=v.ciudad),
		    search.TextField(name="Pais", value=v.pais),
		    search.TextField(name="Idiomas", value=v.idiomas),
		    search.TextField(name="Tags", value=v.tags),
		    search.TextField(name="ID", value=str(i.key.id())),
		    search.DateField(name="Updated", value=datetime.datetime.now().date()),
		    
		    search.NumberField(name="Fee", value=v.fee),
		    search.NumberField(name="Rating", value=v.rating),
		    ]

	d = search.Document(doc_id = str(i.key.id()), fields=fields)
	try:
		index.put(d)
		print 'Documento actualizado'
	except:
		print 'No se pudo crear el indice'	    