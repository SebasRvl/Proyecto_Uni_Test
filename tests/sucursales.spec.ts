import { test, expect } from '@playwright/test';

test('login, search, add to cart, go to home and click item with fa fa-map-marker', async ({ page }) => {
    // Navegar a la página
    await page.goto('https://cuboscubik.com/');
    
    // Hacer clic en el <li> con la clase 'log login'
    const liSelector = 'li.log.login';
    await page.click(liSelector);

    // Esperar a que el input del correo con el id 'input-email' esté visible
    const emailSelector = '#input-email';
    await page.waitForSelector(emailSelector, { state: 'visible' });

    // Rellenar el campo de correo
    await page.fill(emailSelector, 'jilifaj932@cantozil.com');

    // Esperar a que el input de la contraseña con el id 'input-password' esté visible
    const passwordSelector = '#input-password';
    await page.waitForSelector(passwordSelector, { state: 'visible' });

    // Rellenar el campo de contraseña
    await page.fill(passwordSelector, 'MiContraseña123');

    // Esperar a que el botón con la clase 'btn btn-primary pull-left' esté visible
    const buttonSelector = 'input.btn.btn-primary.pull-left';
    await page.waitForSelector(buttonSelector, { state: 'visible' });

    // Hacer clic en el botón
    await page.click(buttonSelector);

    // Esperar a que el <div> con la clase 'logo' esté visible
    const logoSelector = 'div.logo';
    await page.waitForSelector(logoSelector, { state: 'visible' });

    // Hacer clic en el logo para ir a la página principal
    await page.click(logoSelector);

    // Esperar a que el input de búsqueda dentro del <div id="search1"> esté visible
    const searchInputSelector = '#search1 input';  // Buscamos el <input> dentro del <div>
    await page.waitForSelector(searchInputSelector, { state: 'visible' });

    // Asegurarse de que el input esté dentro del área visible (scroll si es necesario)
    const searchInput = await page.$(searchInputSelector);
    await searchInput?.scrollIntoViewIfNeeded();

    // Asegurarse de que el input esté enfocado
    await page.focus(searchInputSelector);

    // Borrar cualquier texto que pueda haber en el input (opcional, solo por seguridad)
    await page.fill(searchInputSelector, '');

    // Escribir "2x2" en el campo de búsqueda
    await page.fill(searchInputSelector, '2x2');

    // Presionar Enter para realizar la búsqueda
    await page.keyboard.press('Enter');

    // Esperar a que el div con la clase 'product-item-container' esté visible
    const productItemSelector = 'div.product-item-container';
    await page.waitForSelector(productItemSelector, { state: 'visible' });

    // Hacer clic en el primer producto (o el que te interese)
    await page.click(productItemSelector);

    // Esperar a que el input con id 'button-cart' esté visible
    const buttonCartSelector = '#button-cart';
    await page.waitForSelector(buttonCartSelector, { state: 'visible' });

    // Hacer clic en el botón de agregar al carrito
    await page.click(buttonCartSelector);

    // Esperar a que el div con la clase 'shopping_cart' esté visible
    const shoppingCartSelector = 'div.shopping_cart';
    await page.waitForSelector(shoppingCartSelector, { state: 'visible' });

    // Hacer clic en el div con la clase 'shopping_cart' para ir al carrito
    await page.click(shoppingCartSelector);

    // Esperar a que el <div> con la clase 'logo' esté visible para volver a la página principal
    await page.waitForSelector(logoSelector, { state: 'visible' });

    // Hacer clic en el logo nuevamente para regresar a la página de inicio
    await page.click(logoSelector);

    // Esperar a que el icono con la clase 'fa fa-map-marker' esté visible
    const mapMarkerSelector = 'i.fa.fa-map-marker';
    await page.waitForSelector(mapMarkerSelector, { state: 'visible' });

    // Hacer clic en el icono de 'map-marker' (ubicación)
    await page.click(mapMarkerSelector);

    // Esperar a que el enlace con el href 'https://maps.app.goo.gl/rnXmYAaQyBueTdxK9' esté visible
    const linkSelector = 'a[href="https://maps.app.goo.gl/rnXmYAaQyBueTdxK9"]';
    await page.waitForSelector(linkSelector, { state: 'visible' });

    // Hacer clic en el enlace
    await page.click(linkSelector);

    // Pausar para inspeccionar después de hacer clic en el enlace
    await page.pause();
});
