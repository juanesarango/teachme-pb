define('frontend/serializers/teacher', ['exports', 'ember-data', 'frontend/serializers/application'], function (exports, DS, ApplicationSerializer) {

  'use strict';

  exports['default'] = ApplicationSerializer['default'].extend(DS['default'].EmbeddedRecordsMixin, {
    attrs: {
      areas: { embedded: "always" }
    } });

});