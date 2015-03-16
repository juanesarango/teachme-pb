define('frontend/models/area', ['exports', 'ember-data'], function (exports, DS) {

  'use strict';

  exports['default'] = DS['default'].Model.extend({
    name: DS['default'].attr("string"),
    namet: DS['default'].attr("string"),
    url: DS['default'].attr("string"),
    checked: DS['default'].attr("boolean")
  });

});