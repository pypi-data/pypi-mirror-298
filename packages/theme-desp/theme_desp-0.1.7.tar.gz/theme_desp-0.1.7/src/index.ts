import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

import favicon from '../style/favicon.png';
import despLogo from '../style/desp-logo.png';
import destinationEarthLogo from '../style/destination-earth.png';
import fundedByEULogo from '../style/funded-by-EU.png';
import implementedByLogo from '../style/implemented-by.png';
import ecmwfLogo from '../style/ecmwf.png';
import esaLogo from '../style/esa.png';
import eumetsatLogo from '../style/eumetsat.png';

import { LightPalletteSetter } from './light-pallette-setter';
import { DarkPalletteSetter } from './dark-pallette-setter';

/**
 * Creates a logo, an 'img' element wrapped by a 'a' element
 */
const createLogo = (logoSrc: string, maxHeight: string, href?: string) => {
  const logoContainer = document.createElement('a');
  logoContainer.href = href || '#';
  logoContainer.target = '_blank';

  const logo = document.createElement('img');
  logo.style.width = 'auto';
  logo.style.maxHeight = maxHeight;
  logo.style.margin = '5px';
  logo.src = logoSrc;

  logoContainer.appendChild(logo);
  return logoContainer;
};

/**
 * Changes the favicon before the application load
 */
const head = document.head;

const favicons = head.querySelectorAll('link[rel="icon"]');
favicons.forEach(favicon => head.removeChild(favicon));

const link: HTMLLinkElement = document.createElement('link');
link.rel = 'icon';
link.type = 'image/x-icon';
link.href = favicon;
head.appendChild(link);

/**
 * Changes the tab title before the application load
 */
let title = head.querySelector('title');
if (!title) {
  title = document.createElement('title');
  head.appendChild(title);
}
title.textContent = 'Insula Code';

/**
 * Add a fixed div that display the user name
 */
const createUserSpan = () => {
  const span = document.createElement('span');

  try {
    const userData = localStorage.getItem(
      '@jupyterlab/services:UserManager#user'
    );

    if (userData) {
      const user = JSON.parse(userData);

      if (user && user.name) {
        span.innerText = user.name;
        span.className = 'user-name-span';
        document.body.appendChild(span);
      }
    }
  } catch (error) {
    console.error('Error parsing user data:', error);
  }
};

createUserSpan();

/**
 * Initialization data for the theme-desp extension
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'theme-desp:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    let footerVisible = true;

    /**
     * Observes changes in the title made elsewhere in the application.
     */
    app.started.then(() => {
      createUserSpan();

      Object.defineProperty(document, 'title', {
        set(arg) {
          Object.getOwnPropertyDescriptor(
            Document.prototype,
            'title'
            // Edit the document.title property setter,
            // call the original setter function for document.title and make sure 'this' is set to the document object,
            // then overrides the value to set
          )?.set?.call(document, 'Insula Code');
        },
        configurable: true
      });
    });

    const showFooter = () => {
      const footer = document.createElement('div');
      footer.classList.add('desp-footer');

      const logo1 = createLogo(
        despLogo,
        '36px',
        'https://destination-earth.eu/'
      );
      const logo2 = createLogo(
        destinationEarthLogo,
        '40px',
        'https://destination-earth.eu/'
      );
      const logo3 = createLogo(
        fundedByEULogo,
        '40px',
        'https://european-union.europa.eu/'
      );
      const logo4 = createLogo(
        implementedByLogo,
        '40px',
        'https://european-union.europa.eu/'
      );
      const logo5 = createLogo(ecmwfLogo, '40px', 'https://www.ecmwf.int/');
      const logo6 = createLogo(esaLogo, '40px', 'https://www.esa.int/');
      const logo7 = createLogo(
        eumetsatLogo,
        '40px',
        'https://www.eumetsat.int/'
      );
      const closeIcon = document.createElement('span');
      closeIcon.textContent = 'x';

      footer.appendChild(logo1);
      footer.appendChild(logo2);
      footer.appendChild(logo3);
      footer.appendChild(logo4);
      footer.appendChild(logo5);
      footer.appendChild(logo6);
      footer.appendChild(logo7);
      footer.appendChild(closeIcon);

      closeIcon.addEventListener('click', () => {
        document.body.removeChild(footer);
        footerVisible = false;
        showOpenButton();
      });

      document.body.appendChild(footer);
      footerVisible = true;
    };

    const showOpenButton = () => {
      if (document.getElementById('desp-footer-open-button')) return;

      const reopenButton = document.createElement('img');
      reopenButton.id = 'desp-footer-open-button';
      reopenButton.src = despLogo;
      reopenButton.classList.add('desp-footer-open-button');

      reopenButton.addEventListener('click', () => {
        document.body.removeChild(reopenButton);
        showFooter();
      });

      document.body.appendChild(reopenButton);
    };

    if (footerVisible) {
      showFooter();
    } else {
      showOpenButton();
    }

    /**
     * Due to the current limitation of not being able to register multiple themes
     * (https://github.com/jupyterlab/jupyterlab/issues/14202)
     * in the same extension when each theme has its own separate CSS file, we
     * handle theme variants by storing the color palette in TypeScript files and
     * loading them dynamically through a script. This approach allows us to load
     * a base theme ('theme-desp/index.css') and then override the necessary color properties
     * based on the selected palette.
     */
    const pallettesSetters = [LightPalletteSetter, DarkPalletteSetter];
    const baseTheme = 'theme-desp/index.css';

    pallettesSetters.forEach(Pallette => {
      const pallette = new Pallette();
      manager.register({
        name: pallette.name,
        isLight: pallette.type === 'light',
        load: () => {
          pallette.setColorPallette();
          return manager.loadCSS(baseTheme);
        },
        unload: () => Promise.resolve(undefined)
      });
    });
  }
};

export default plugin;
