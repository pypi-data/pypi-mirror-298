/**
 * @typedef AttributeDef
 * @property {string} name
 * @property {string?} [key]
 * @property {unknown?} [value]
 */

/**
 * @typedef StyleDef
 * @property {string} name
 * @property {string?} [key]
 * @property {unknown?} [value]
 */

/**
 * @typedef EventDef
 * @property {string} name
 * @property {string[]?} [keys]
 */

/**
 * @typedef ElementDef
 * @property {string} tag
 * @property {AttributeDef[]?} [attributes]
 * @property {StyleDef[]?} [styles]
 * @property {EventDef[]?} [events]
 */

/**
 * @typedef BaseContext
 * @property {boolean?} [_use_iframe]
 * @property {ElementDef} _element
 * @property {ElementDef[]} _meta_elements
 * @property {string?} width
 * @property {string?} height
 */

/**
 * @typedef {BaseContext & Record<string, any>} Context
 */

/**
 * @typedef {import("npm:@anywidget/types").AnyModel<Context>} Model
 */

function shared() {
  /** @type {(value: any) => any} */
  function serializeAttributeValue(value) {
    try {
      if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value);
      }
    } catch {
      console.warn('Unable to json encode attribute object', value);
      return null;
    }

    return value;
  }

  /** @type {(el: HTMLElement, name: string, value: any) => void} */
  function updateAttribute(el, name, value) {
    value = serializeAttributeValue(value);
    if (value !== null && value !== undefined) {
      el.setAttribute(name, value);
    } else {
      el.removeAttribute(name);
    }
  }

  /** @type {(model: Model, def: AttributeDef | StyleDef) => any} */
  function getInitialValue(model, def) {
    const { key, value } = def;
    const modelValue = key ? model.get(key) : null;
    return modelValue ?? value;
  }

  /** @type {(el: HTMLElement, model: Model, def: AttributeDef) => void} */
  function initializeAttribute(el, model, def) {
    const { name, key } = def;

    updateAttribute(el, name, getInitialValue(model, def));
    if (key) {
      model.on(`change:${key}`, () => updateAttribute(el, name, model.get(key)));
    }
  }

  /** @type {(el: HTMLElement, name: string, value: any) => void} */
  function updateStyle(el, name, value) {
    if (value !== null && value !== undefined) {
      el.style.setProperty(name, `${value}`);
    } else {
      el.style.removeProperty(name);
    }
  }

  /** @type {(el: HTMLElement, model: Model, def: StyleDef) => void} */
  function initializeStyle(el, model, def) {
    const { name, key } = def;

    updateStyle(el, name, getInitialValue(model, def));
    if (key) {
      model.on(`change:${key}`, () => updateStyle(el, name, model.get(key)));
    }
  }

  /** @type {(event: Record<string, unknown>, keys: string[] | null | undefined) => unknown} */
  function selectEventData(event, keys) {
    keys ??= ['detail'];
    if (keys.length === 1) {
      return event[keys[0]];
    }

    /** @type Record<string, unknown> */
    const data = {};
    for (const key of keys) {
      data[key] = event[key];
    }

    return data;
  }

  /** @type {(el: HTMLElement, model: Model, def: EventDef) => void} */
  function initializeEvent(el, model, def) {
    const { name, keys } = def;
    el.addEventListener(name, (event) => {
      model.send({ event: name, data: selectEventData(/** @type {any} */ (event), keys) });
    });
  }

  /** @type {(parent: HTMLElement, model: Model, def: ElementDef) => HTMLElement | null} */
  function findElement(parent, model, def) {
    let selector = def.tag;
    def.attributes?.forEach((attrDef) => {
      let value = getInitialValue(model, attrDef);
      if (value !== null && value !== undefined) {
        value = serializeAttributeValue(value);
        selector += `[${attrDef.name}="${value}"]`;
      }
    });

    return parent.querySelector(selector);
  }

  /** @type {(parent: HTMLElement, model: Model, def: ElementDef, once?: boolean) => HTMLElement} */
  function initializeElement(parent, model, def, once = false) {
    if (!def.tag) {
      throw new Error('Bad element definition');
    } else if (once) {
      const el = findElement(parent, model, def);
      if (el) {
        return el;
      }
    }

    const el = document.createElement(def.tag);
    def.attributes?.forEach((attrDef) => initializeAttribute(el, model, attrDef));
    def.styles?.forEach((styleDef) => initializeStyle(el, model, styleDef));
    def.events?.forEach((eventDef) => initializeEvent(el, model, eventDef));
    parent.appendChild(el);
    return el;
  }

  /** @type {(el: HTMLElement) => Promise<void>} */
  async function whenLoaded(el) {
    await new Promise((res, rej) => {
      el.addEventListener('load', res);
      el.addEventListener('error', rej);
    });
  }

  /** @type {(el: HTMLElement, timeout: number) => Promise<void>} */
  async function whenStable(el, timeout) {
    const timer = new Promise((res) => setTimeout(res, timeout));
    const whenStableImpl = async () => {
      await customElements.whenDefined(el.localName);
      if ('whenStable' in el && typeof el.whenStable === 'function') {
        await el.whenStable();
      }
    };

    await Promise.race([whenStableImpl(), timer]);
  }

  return {
    serializeAttributeValue,
    updateAttribute,
    getInitialValue,
    initializeAttribute,
    updateStyle,
    initializeStyle,
    selectEventData,
    initializeEvent,
    findElement,
    initializeElement,
    whenLoaded,
    whenStable,
  };
}

/** @type {import("npm:@anywidget/types").Render<Context>} */
async function renderInline(context) {
  const { initializeElement, whenLoaded, whenStable } = shared();
  const { model, el } = context;
  const { head } = document;
  const promises = /** @type {Promise<any>[]} */ ([]);

  for (const def of model.get('_meta_elements')) {
    const el = initializeElement(head, model, def, true);
    promises.push(whenLoaded(el));
  }

  const instance = initializeElement(el, model, model.get('_element'));
  promises.push(whenStable(instance, 750));

  await Promise.all(promises);
}

/** @type {import("npm:@anywidget/types").Render<Context>} */
async function renderIframe(context) {
  const { initializeElement, whenLoaded } = shared();
  const iframeTemplate = `<!DOCTYPE html>
  <html>
    <head>
      <script>
        ${shared.toString()}
        ${renderInline.toString()}
        globalThis.render = ${renderInline.name};
      </script>
    </head>
    <body></body>
  </html>`;
  /** @type {ElementDef} */
  const iframeElementDef = {
    tag: 'iframe',
    attributes: [
      {
        name: 'srcdoc',
        value: iframeTemplate,
      },
    ],
    styles: [
      {
        name: 'width',
        key: 'width',
      },
      {
        name: 'height',
        key: 'height',
      },
      {
        name: 'border',
        value: 'none',
      },
    ],
  };

  const iframe = /** @type {HTMLIFrameElement} */ (initializeElement(context.el, context.model, iframeElementDef));
  await whenLoaded(iframe);

  const hraApp = /** @type {{render: typeof renderInline} & Window} */ (iframe.contentWindow);
  await hraApp.render({
    ...context,
    el: iframe.contentDocument?.body ?? context.el,
  });
}

/** @type {import("npm:@anywidget/types").Render<Context>} */
async function render(context) {
  const useIframe = context.model.get('_use_iframe') ?? false;
  const impl = useIframe ? renderIframe : renderInline;
  await impl(context);
}

export default { render };
