"use strict";
(self["webpackChunkpergamon_theme"] = self["webpackChunkpergamon_theme"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Initialization data for the pergamon_theme extension.
 */
const plugin = {
    id: 'pergamon_theme:plugin',
    description: 'Pergamon Theme Extension.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: (app, manager) => {
        console.log('JupyterLab extension pergamon_theme is activated!');
        const style = 'pergamon_theme/index.css';
        manager.register({
            name: 'pergamon_theme',
            isLight: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
        manager.setTheme('pergamon_theme');
        setTimeout(() => {
            var _a;
            const bottomBarLeft = document.getElementsByClassName('jp-StatusBar-Left')[0];
            // apply simple UI
            if (bottomBarLeft) {
                const switchElement = bottomBarLeft.getElementsByClassName('jp-switch')[0];
                if (switchElement.getAttribute('aria-checked') === 'false') {
                    switchElement === null || switchElement === void 0 ? void 0 : switchElement.dispatchEvent(new Event('click'));
                }
                (_a = bottomBarLeft === null || bottomBarLeft === void 0 ? void 0 : bottomBarLeft.parentNode) === null || _a === void 0 ? void 0 : _a.removeChild(bottomBarLeft);
            }
            [
                document.getElementsByClassName('jp-StatusBar-Right')[0],
                document.querySelector('.jp-mod-right [data-id="jp-property-inspector"]'),
                document.querySelector('.jp-mod-right [data-id="jp-debugger-sidebar"]'),
                document.querySelector('#jp-title-panel-title') // default title
            ].forEach(element => {
                var _a;
                (_a = element === null || element === void 0 ? void 0 : element.parentNode) === null || _a === void 0 ? void 0 : _a.removeChild(element);
            });
        }, 500);
        // Create a custom loading screen element
        const customLoadingScreen = document.createElement('div');
        customLoadingScreen.className = 'custom-loading-screen';
        customLoadingScreen.textContent = 'Loading, please wait...';
        // Add the custom loading screen to the document
        document.body.appendChild(customLoadingScreen);
        const splashElement = document.querySelector('.jp-Splash');
        if (splashElement) {
            splashElement.remove();
        }
        // Remove the custom loading screen once JupyterLab is fully loaded
        app.restored.then(() => {
            document.body.removeChild(customLoadingScreen);
        });
        const observer = new MutationObserver((mutationsList, observer) => {
            const splashElement = document.querySelector('.jp-Splash');
            if (splashElement) {
                splashElement.remove();
                observer.disconnect();
            }
        });
        // @ts-expect-error error
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.NotificationManager.prototype.notify = function () {
            // No hacer nada
            console.log('Notificación bloqueada.');
        };
        observer.observe(document.body, { childList: true, subtree: true });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.7d13f0a2c1e79232abd6.js.map