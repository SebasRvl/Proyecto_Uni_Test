import { test, expect } from '@playwright/test';

test('download wallpaper', async ({ page }) => {
    // Navegar a la página
    await page.goto('https://cuboscubik.com/');

    // Esperar a que el <li> con la clase 'checkout hidden-xs' esté visible
    const liSelector = 'li.checkout.hidden-xs';
    await page.waitForSelector(liSelector, { state: 'visible' });

    // Desplazar el <li> a la vista para asegurarse de que esté visible
    const liElement = await page.$(liSelector);
    await liElement?.scrollIntoViewIfNeeded();

    // Hacer clic en el <li>
    await page.click(liSelector);

    // Esperar a que el enlace con href 'https://cuboscubik.com/image/catalog/fondos-pantalla/cuboscubik-wallpaper-1-cel.png' esté visible
    const downloadLinkSelector = 'a[href="https://cuboscubik.com/image/catalog/fondos-pantalla/cuboscubik-wallpaper-1-cel.png"]';
    await page.waitForSelector(downloadLinkSelector, { state: 'visible' });

    // Hacer clic en el enlace para descargar el fondo
    await page.click(downloadLinkSelector);

    // Pausar para inspeccionar después de hacer clic en el enlace
    await page.pause();
});
