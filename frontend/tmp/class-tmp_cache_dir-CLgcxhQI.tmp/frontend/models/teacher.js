define('frontend/models/teacher', ['exports', 'ember-data'], function (exports, DS) {

  'use strict';

  exports['default'] = DS['default'].Model.extend({
    name: DS['default'].attr("string"),
    lname: DS['default'].attr("string"),
    mail: DS['default'].attr("string"),
    about: DS['default'].attr("string"),
    fee: DS['default'].attr("number"),
    profilePic: DS['default'].attr("string"),
    ciudad: DS['default'].attr("string"),
    pais: DS['default'].attr("string"),
    idiomas: DS['default'].attr("string"),
    linkedin: DS['default'].attr("string"),
    areas: DS['default'].hasMany("area"),
    timezoneOffset: DS['default'].attr("number"),
    tags: DS['default'].attr("string"),
    dateAvailable: DS['default'].attr("string"),
    dateReserved: DS['default'].attr("number"),
    teachouts: DS['default'].attr("number"),
    teachoutsExpired: DS['default'].attr("number"),
    rating: DS['default'].attr("number"),
    // reviews: DS.hasMany('review'),
    score: DS['default'].attr("number"),
    aceptado: DS['default'].attr("boolean"),
    movil: DS['default'].attr("number")
  });

});