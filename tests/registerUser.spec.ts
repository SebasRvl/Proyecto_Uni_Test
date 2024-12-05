const { test, expect } = require('@playwright/test');

test('register', async ({ page }) => {
  // Navegar a la página
  await page.goto('https://cuboscubik.com/');

  // Hacer clic en el <li> con la clase 'regis'
  const liSelector = 'li.regis';
  await page.click(liSelector);

  // Esperar a que el input del nombre con el id 'input-firstname' esté visible
  const firstnameSelector = '#input-firstname';
  await page.waitForSelector(firstnameSelector, { state: 'visible' });

  // Asegurarse de que el input del nombre no esté deshabilitado
  const isFirstnameDisabled = await page.$eval(firstnameSelector, el => el.disabled);
  if (isFirstnameDisabled) {
    console.log('El input del nombre está deshabilitado');
    return;
  }

  // Escribir el nombre en el campo de texto
  await page.fill(firstnameSelector, 'Juan');

  // Esperar a que el input del apellido con el id 'input-lastname' esté visible
  const lastnameSelector = '#input-lastname';
  await page.waitForSelector(lastnameSelector, { state: 'visible' });

  // Asegurarse de que el input del apellido no esté deshabilitado
  const isLastnameDisabled = await page.$eval(lastnameSelector, el => el.disabled);
  if (isLastnameDisabled) {
    console.log('El input del apellido está deshabilitado');
    return;
  }

  // Escribir el apellido en el campo de texto
  await page.fill(lastnameSelector, 'Pérez');

  // Esperar a que el input del email con el id 'input-email' esté visible
  const emailSelector = '#input-email';
  await page.waitForSelector(emailSelector, { state: 'visible' });

  // Asegurarse de que el input del email no esté deshabilitado
  const isEmailDisabled = await page.$eval(emailSelector, el => el.disabled);
  if (isEmailDisabled) {
    console.log('El input del email está deshabilitado');
    return;
  }

  // Escribir el email en el campo de texto
  await page.fill(emailSelector, 'jilifaj932@cantozil.com');

  // Esperar a que el input del teléfono con el id 'input-telephone' esté visible
  const telephoneSelector = '#input-telephone';
  await page.waitForSelector(telephoneSelector, { state: 'visible' });

  // Asegurarse de que el input del teléfono no esté deshabilitado
  const isTelephoneDisabled = await page.$eval(telephoneSelector, el => el.disabled);
  if (isTelephoneDisabled) {
    console.log('El input del teléfono está deshabilitado');
    return;
  }

  // Escribir el teléfono en el campo de texto
  await page.fill(telephoneSelector, '5512345678');

  // Esperar a que el input de la contraseña con el id 'input-password' esté visible
  const passwordSelector = '#input-password';
  await page.waitForSelector(passwordSelector, { state: 'visible' });

  // Asegurarse de que el input de la contraseña no esté deshabilitado
  const isPasswordDisabled = await page.$eval(passwordSelector, el => el.disabled);
  if (isPasswordDisabled) {
    console.log('El input de la contraseña está deshabilitado');
    return;
  }

  // Escribir la contraseña en el campo de texto
  await page.fill(passwordSelector, 'MiContraseña123');

  // Esperar a que el input de confirmación de la contraseña con el id 'input-confirm' esté visible
  const confirmPasswordSelector = '#input-confirm';
  await page.waitForSelector(confirmPasswordSelector, { state: 'visible' });

  // Asegurarse de que el input de confirmación de la contraseña no esté deshabilitado
  const isConfirmPasswordDisabled = await page.$eval(confirmPasswordSelector, el => el.disabled);
  if (isConfirmPasswordDisabled) {
    console.log('El input de confirmación de la contraseña está deshabilitado');
    return;
  }

  // Escribir la confirmación de la contraseña en el campo de texto
  await page.fill(confirmPasswordSelector, 'MiContraseña123');

  // Esperar a que el checkbox con el name 'agree' esté visible
  const checkboxSelector = 'input[name="agree"]';
  await page.waitForSelector(checkboxSelector, { state: 'visible' });

  // Marcar el checkbox
  await page.check(checkboxSelector);

  // Esperar a que el botón con la clase 'btn btn-primary' esté visible
  const buttonSelector = 'input.btn.btn-primary'; // Seleccionamos el botón por su clase
  await page.waitForSelector(buttonSelector, { state: 'visible' });

  // Hacer clic en el botón
  await page.click(buttonSelector);

  // Pausar para inspeccionar la página después de la acción
  await page.pause();
});
