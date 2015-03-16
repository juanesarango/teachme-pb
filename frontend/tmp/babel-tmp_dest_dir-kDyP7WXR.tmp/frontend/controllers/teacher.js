import Ember from "ember";

export default Ember.ObjectController.extend({
  isEditable: true,
  isAboutEditable: true,
  isFeeEditable: true,
  actions: {
    toogleEditable: function toogleEditable(property) {
      this.toggleProperty(property);
    }
  }
});