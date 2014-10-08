# -*- coding: utf-8 -*-
from google.appengine.api import search
from google.appengine.ext import ndb
import teachme_db
import datetime
import fns

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
				astr.append(fns.normalise_unicode(a.name))	
	return list2string(astr)

def create_index(entity=None):
	index = search.Index(name=_INDEX_NAME)
	if entity:
		teachers = [entity]
	else:
		teachers = teachme_db.teacher.query()

	for i in teachers:
		
		fields = [
		    search.TextField(name="Nombre", value=i.name+" "+i.lname),
		    search.TextField(name="Ciudad", value=i.ciudad),
		    search.TextField(name="Pais", value=i.pais),
		    search.TextField(name="Area", value=id2str_areas(i.areas)),
		    search.TextField(name="Tags", value=list2string(i.tags)),
		    search.TextField(name="key", value=i.key.urlsafe()),
		    search.DateField(name="Updated", value=datetime.datetime.now().date()),
		    ]

		d = search.Document(doc_id = i.key.urlsafe(), fields=fields)

		try:
			index.put(d)
			# print 'Indice creado'
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
  		# if number_found ==1:
  		# 	print 'Se encontro ' +  str(number_found) + ' resultado'	
  		# else:
  		# 	print 'Se encontraron ' +  str(number_found) + ' resultados'
		return search_results
	except search.Error:
		print 'No se encontraron resultados'



def delete_index(ids):
	index = search.Index(name=_INDEX_NAME)
	index.delete(document_ids=ids) 

def update_index(entity, field_name, field_value, replace=False):
	index = search.Index(name=_INDEX_NAME)
	document  = index.get(entity.key.urlsafe())
	if document:	
		fields = document.fields
		new_fields = []
		for f in fields:
			if f.name==field_name:
				if replace:
					new_fields.append(search.TextField(name=field_name, value=field_value))
				else:
					new_fields.append(search.TextField(name=field_name, value=f.value+""+field_value))
			else:
				new_fields.append(f)
		new_doc = search.Document(doc_id=entity.key.urlsafe(), fields=new_fields)
		try:
			index.put(new_doc)
			# print 'Documento actualizado: se actualizo el campo '+ field_name
		except:
			print 'No se pudo crear el indice'
	else:
		print 'Esta entidad no esta indexada'	
