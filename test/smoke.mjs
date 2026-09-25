// Опциональный smoke-тест (нужен Playwright: npm i -D playwright && npx playwright install chromium)
// Запуск: node test/smoke.mjs
// Проверяет: страница грузится, нет ошибок консоли, canvas создан, меню видно, старт уровня работает.
const run = async () => {
  let chromium
  try { ({ chromium } = await import('playwright')) }
  catch { console.log('SKIP: playwright не установлен'); process.exit(0) }
  const url = process.env.URL || 'http://localhost:8080/index.html'
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } })
  const errors = []
  page.on('pageerror', e => errors.push('pageerror: ' + e.message))
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()) })
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.waitForSelector('#gl canvas', { timeout: 20000 })
  await page.waitForSelector('#menu.active', { timeout: 20000 })
  const fatal = await page.isVisible('#fatal.show').catch(() => false)
  if (fatal) errors.push('показана панель фатальной ошибки')
  await page.click('#btnPlay')
  await page.waitForSelector('#hud.active', { timeout: 20000 })
  await page.waitForTimeout(3000)
  const herd = await page.textContent('#hHerd')
  const time = await page.textContent('#hTime')
  await page.keyboard.down('KeyW'); await page.waitForTimeout(1200); await page.keyboard.up('KeyW')
  await page.keyboard.down('KeyD'); await page.waitForTimeout(1200); await page.keyboard.up('KeyD')
  console.log('HUD: стадо=' + herd + ' таймер=' + time)
  await page.keyboard.press('Escape')
  await page.waitForSelector('#pause.active', { timeout: 5000 })
  await browser.close()
  if (errors.length) { console.error('SMOKE FAILED:\n' + errors.join('\n')); process.exit(1) }
  console.log('✔ SMOKE PASSED')
}
run()
