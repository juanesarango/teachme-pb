define('frontend/adapters/application', ['exports', 'ember-data'], function (exports, DS) {

	'use strict';

	exports['default'] = DS['default'].RESTAdapter.extend({
		namespace: "_ah/api/teachme/v1"
	});

});