# -*- coding: utf-8 -*-
from google.appengine.api import search
from google.appengine.ext import ndb
import teachme_db
import datetime

_INDEX_NAME = 'Profesores'

def list2string(listvar):
	stringvar=""
	for l in listvar:
		stringvar=stringvar+l+" "
	return stringvar

def id2str_areas(ids):
	areas = teachme_db.areas.query().order(teachme_db.areas.name)
	astr = []
	for a in areas:
		for aid in ids:
			if aid==a.key.id():
				astr.append(a.name)
				if (a.name == u"Matemáticas"):
					astr.append(u"Matematicas")
				elif (a.name == u"Física"):
					astr.append(u"Fisica")
				elif (a.name == u"Biología"):
					astr.append(u"Biologia")
				elif (a.name == u"Música"):
					astr.append(u"Musica")
				elif (a.name == u"Química"):
					astr.append(u"Quimica")		
	return list2string(astr)

def create_index():
	index = search.Index(name=_INDEX_NAME)

	for i in teachme_db.teacher.query():
		
		fields = [
		    search.TextField(name="Nombre", value=i.name+" "+i.lname),
		    search.TextField(name="Ciudad", value=i.ciudad),
		    search.TextField(name="Pais", value=i.pais),
		    # search.TextField(name="Idiomas", value=list2string(i.idiomas)),
		    search.TextField(name="Area", value=id2str_areas(i.areas)),
		    search.TextField(name="Tags", value=list2string(i.tags)),
		    search.TextField(name="key", value=i.key.urlsafe()),
		    search.DateField(name="Updated", value=datetime.datetime.now().date()),
		    
		    # search.NumberField(name="Fee", value=i.fee),
		    # search.NumberField(name="Rating", value=i.rating),
		    ]

		d = search.Document(doc_id = i.key.urlsafe(), fields=fields)

		try:
			index.put(d)
			print 'Indice creado'
		except:
			print 'No se pudo crear el indice'

def make_query(query_string, doc_limit=10):

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
  		else:
  			print 'Se encontraron ' +  str(number_found) + ' resultados'
		# for document in search_results:
		# 	print u"Document_id: {doc_id}\n".format(doc_id=document.doc_id)
		# 	for f in document.fields:
		# 		print u"{nombre_campo}: {valor_campo}\n".format(nombre_campo=f.name,valor_campo=f.value)
		return search_results
	except search.Error:
		print 'No se encontraron resultados'

def edit_index(id, field_name, field_value):
	index = search.Index(name=_INDEX_NAME)
	try:
		i = ndb.Key(urlsafe = str(id)).get()
	except ProtocolBufferDecodeError, e:
		 i = ndb.Key('teacher',long(id))
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

	d = search.Document(doc_id = id, fields=fields)
	try:
		index.put(d)
		print 'Documento actualizado'
	except:
		print 'No se pudo crear el indice'

def delete_index(ids):
	index = search.Index(name=_INDEX_NAME)
	index.delete(document_ids=ids)    