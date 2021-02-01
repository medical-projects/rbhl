angular.module('opal.controllers').controller(
  'BloodsStep', function(scope, step, episode, $window, $location, $modal, displayDateFilter) {
  "use strict"
  /*
  * The bloods step works on a single bloods instance.
  * if there is an id as a GET param in the url, then it is that instance
  * otherwise we create a new one.
  */
  var init = function(){
    var bloodTest;
    scope.bloodTest = null;
    var id = $location.search().id;
    if(!id){
      bloodTest = {};
    }
    else{
      bloodTest = _.findWhere(scope.editing.bloods, {id: parseInt(id)});
      if(!bloodTest){
        alert('Unable to find bloods');
      }
    }
    scope.bloodTest = {bloods: bloodTest};
  }

  scope.employer_display = function(employment){
    var result;
    if(employment.employer && employment.oh_provider){
      result = employment.employer + "/" + employment.oh_provider;
    }
    else{
      result = employment.employer || employment.oh_provider;
    }
    if(employment.job_title){
      result += " (" + employment.job_title + ")";
    }
    return result;
  }

  scope.referral_display = function(referral){
    var result = displayDateFilter(referral.date_of_referral) || "";
    result = result + " " + referral.referrer_name;
    if(result && referral.reference_number){
      result += " (" + referral.reference_number + ")";
    }
    return result;
  }

  scope.addSubrecord = function(subrecordName){
    /*
    * The form has a select box to choo
    *
    *
    * Employer used to be a singleton
    * if there is a model with no creted timestamp
    * use that rather than creating a new employment model
    */
    var subrecordSet = episode[subrecordName];
    var subrecord = _.find(subrecordSet, function(subrecord){
      return !subrecord.created && !subrecord.updated;
    });
    if(subrecord){
      episode.recordEditor.editItem(subrecordName, subrecord).then(function(result){
        if(result == 'deleted' || result == 'cancel'){
          return;
        }
        var field = subrecordName + "_id";
        scope.bloodTest.bloods[field] = subrecord.id;
      });
    }
    else{
      var idsBefore = _.pluck(subrecordSet, "id");
      episode.recordEditor.newItem(subrecordName).then(function(result){
        if(result == 'deleted' || result == 'cancel'){
          return;
        }
        // find the new id that's been added
        var idsAfter = _.pluck(episode[subrecordName], "id");
        var newIds = _.difference(idsAfter, idsBefore);
        if(newIds.length){
          var field = subrecordName + "_id";
          scope.bloodTest.bloods[field] = newIds[0];
        }
      });
    }
  }

  scope.addResult = function(){
    if(!scope.bloodTest.bloods.bloodresult){
      scope.bloodTest.bloods.bloodresult = [];
    }
    scope.bloodTest.bloods.bloodresult.push({});
  }

  scope.removeResult = function(idx){
    scope.bloodTest.bloods.bloodresult.splice(idx, 1);
  }

  scope.selectAllergen = function($item, result){
    if($item){
      result.antigenno = $item.code
    }
  }


  scope.delete = function(){
    var item = _.findWhere(episode.bloods, {id: scope.bloodTest.bloods.id})
    var deleteModal =  $modal.open({
      templateUrl: '/templates/pathway/delete_bloods_modal.html',
      controller: 'DeleteItemConfirmationCtrl',
      resolve: {
        item: item
      }
    });
    deleteModal.result.then(function(result){
      if(result === 'deleted'){
        $window.location.href = "/#/patient/" + item.patient_id + "/investigations";
      }
    });
  }

  scope.preSave = function(editing){
    var urlId = $location.search().id;
    urlId = parseInt(urlId);

    // there should always be a bloodTest but potentially
    // if it was unable to find the bloods then this
    // would not be the case.
    if(scope.bloodTest){
      if(urlId){
        var idx = _.findIndex(editing.bloods, function(bb){
          return bb.id === urlId;
        });
        editing.bloods[idx] = scope.bloodTest.bloods;
      }
      else{
        editing.bloods.push(scope.bloodTest.bloods);
      }
    }
  }

  init();
});