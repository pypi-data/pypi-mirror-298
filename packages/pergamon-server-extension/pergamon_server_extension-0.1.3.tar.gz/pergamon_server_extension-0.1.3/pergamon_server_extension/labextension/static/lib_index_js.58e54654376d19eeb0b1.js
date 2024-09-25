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
                    session.kernel.requestExecute({
                        code: '%load_ext jupyter_ai'
                    });
                }
            });
        });
        const customLoadingScreen = document.createElement('div');
        customLoadingScreen.className = 'custom-loading-screen';
        customLoadingScreen.textContent = 'Loading, please wait...';
        // Add the custom loading screen to the document
        document.body.appendChild(customLoadingScreen);
        // const splashElement = document.querySelector('.jp-Splash');
        window.onload = function () {
            const splashElement = document.querySelector('.jp-Splash');
            console.log(splashElement);
            if (splashElement) {
                splashElement.remove(); // O cualquier acción que quieras realizar
            }
        };
        // if (splashElement) {
        //   splashElement.remove();
        // }
        // app.restored.then(() => {
        //   document.body.removeChild(customLoadingScreen);
        // });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.58e54654376d19eeb0b1.js.map