"use strict";
(self["webpackChunkpergamon_server_extension"] = self["webpackChunkpergamon_server_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Initialization data for the pergamon_server_extension extension.
 */
const plugin = {
    id: 'pergamon_server_extension:plugin',
    description: 'Calliope server extension',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, tracker) => {
        console.log('JupyterLab extension pergamon_server_extension is activated!');
        tracker.widgetAdded.connect((sender, notebookPanel) => {
            notebookPanel.sessionContext.ready.then(() => {
                const session = notebookPanel.sessionContext.session;
                if (session === null || session === void 0 ? void 0 : session.kernel) {
                    // loads the extension
                    session.kernel.requestExecute({
                        code: '%load_ext jupyter_ai'
                    });
                    // set aliases
                    session.kernel.requestExecute({
                        code: '%ai register openai '
                    });
                }
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.2fdd5fd66fe378edd543.js.map