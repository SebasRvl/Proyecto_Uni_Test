import { test, expect } from '@playwright/test';

test('login', async ({ page }) => {
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

    // Pausar para inspeccionar la página después del clic
    await page.pause();
});
