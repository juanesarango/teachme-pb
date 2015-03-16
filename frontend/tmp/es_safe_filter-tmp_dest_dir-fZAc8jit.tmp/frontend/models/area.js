import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  namet: DS.attr('string'),
  url: DS.attr('string'),
  checked: DS.attr('boolean')
});
