import DS from "ember-data";
import Ember from "ember";

export default DS.RESTSerializer.extend({

	serializeIntoHash: function serializeIntoHash(hash, type, record, options) {
		Ember.merge(hash, this.serialize(record, options));
	} });