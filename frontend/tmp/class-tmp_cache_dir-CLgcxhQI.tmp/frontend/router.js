define('frontend/router', ['exports', 'ember', 'frontend/config/environment'], function (exports, Ember, config) {

  'use strict';

  var Router = Ember['default'].Router.extend({
    location: config['default'].locationType
  });

  Router.map(function () {
    this.resource("teacher", { path: "/teacher/:teacher_id" }, function () {});
    this.resource("area", function () {});
  });

  exports['default'] = Router;

});