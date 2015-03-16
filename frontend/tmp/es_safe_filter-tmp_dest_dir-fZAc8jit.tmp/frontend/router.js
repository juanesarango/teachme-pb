import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.resource("teacher", { path: '/teacher/:teacher_id' }, function() { });
  this.resource('area', function() {});
});

export default Router;
