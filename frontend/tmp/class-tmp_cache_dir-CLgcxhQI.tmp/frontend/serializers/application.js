define('frontend/serializers/application', ['exports', 'ember-data', 'ember'], function (exports, DS, Ember) {

	'use strict';

	exports['default'] = DS['default'].RESTSerializer.extend({

		serializeIntoHash: function serializeIntoHash(hash, type, record, options) {
			Ember['default'].merge(hash, this.serialize(record, options));
		} });

});