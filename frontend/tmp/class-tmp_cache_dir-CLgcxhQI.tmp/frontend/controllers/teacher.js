define('frontend/controllers/teacher', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].ObjectController.extend({
    isEditable: true,
    isAboutEditable: true,
    isFeeEditable: true,
    actions: {
      toogleEditable: function toogleEditable(property) {
        this.toggleProperty(property);
      }
    }
  });

});