"use strict";

const ActionView = Spina.spina(class extends RB.Actions.ActionView {
  static events = {
    'click': 'waitIt'
  };
  async waitIt(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    if (confirm(gettext("Are you sure you want to ShipIt?"))) {
      const page = RB.PageManager.getPage();
      const pageModel = page.model;
      const pendingReview = pageModel.get('pendingReview');
      await pendingReview.ready();
      pendingReview.set({
        bodyTop: gettext("Ship It!"),
        shipIt: true
      });
      const comment = pendingReview.createGeneralComment(undefined, true);
      comment.set({
        text: gettext("Wait for CI!")
      });
      await comment.save();
      await pendingReview.publish();
      const reviewRequest = pageModel.get('reviewRequest');
      RB.navigateTo(reviewRequest.get('reviewURL'));
    }
    return false;
  }
});
ExtendedApprovalExtension = {
  ActionView
};

//# sourceMappingURL=extension.js.map