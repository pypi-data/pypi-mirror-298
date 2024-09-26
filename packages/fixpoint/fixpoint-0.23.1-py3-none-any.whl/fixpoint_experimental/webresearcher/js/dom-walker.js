// const walkUpDomTree = async (locator) => {
async (allElems) => {
  const pullDataAttributes = (el) => {
    const dataAttributes = {};
    for (const attr of el.attributes) {
      if (attr.name.startsWith("data-")) {
        dataAttributes[attr.name] = attr.value;
      }
    }
    return dataAttributes;
  };

  const walkUpElemDom = (starterElem) => {
    const path = [];
    let currentElement = starterElem;

    while (currentElement && currentElement !== document.documentElement) {
      const parentElement = currentElement.parentElement;

      if (!parentElement) break;

      const siblings = Array.from(parentElement.children);
      const isOnlySibling = siblings.length === 1;

      path.unshift({
        tag: currentElement.tagName.toLowerCase(),
        id: currentElement.id,
        classes: Array.from(currentElement.classList),
        dataAttributes: pullDataAttributes(currentElement),
      });

      currentElement = parentElement;
    }

    // Always include the HTML element
    path.unshift({
      tag: "html",
      id: document.documentElement.id,
      classes: Array.from(document.documentElement.classList),
      dataAttributes: pullDataAttributes(document.documentElement),
    });

    return path;
  };

  return allElems.map(walkUpElemDom);
};
