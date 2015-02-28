import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  lname: DS.attr('string'),
  mail: DS.attr('string'),
  about: DS.attr('string'),
  fee: DS.attr('number'),
  profilePic: DS.attr('string'),
  ciudad: DS.attr('string'),
  pais: DS.attr('string'),
  idiomas: DS.attr('string'),
  linkedin: DS.attr('string'),
  areas: DS.hasMany('area'),
  timezoneOffset: DS.attr('number'),
  tags: DS.attr('string'),
  dateAvailable: DS.attr('string'),
  dateReserved: DS.attr('number'),
  teachouts: DS.attr('number'),
  teachoutsExpired: DS.attr('number'),
  rating: DS.attr('number'),
  // reviews: DS.hasMany('review'),
  score: DS.attr('number'),
  aceptado: DS.attr('boolean'),
  movil: DS.attr('number')
});
