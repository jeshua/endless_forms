const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });

    await page.goto('http://localhost:3000');
    await page.waitForTimeout(2000);

    // Test Triangle styles with 3D view
    console.log('--- TRIANGLE ---');
    await page.click('button:has-text("Triangle")');
    await page.waitForTimeout(500);

    // Capture 3D view of classic style to see slotting
    await page.selectOption('#styleSelect', 'classic');
    await page.waitForTimeout(500);
    await page.click('button:has-text("3D")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: `tri-classic-3d-merged.png` });
    console.log('Triangle classic: 3D merged');

    await page.click('button:has-text("Apart")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: `tri-classic-3d-apart.png` });
    console.log('Triangle classic: 3D apart');

    // Back to top view for other styles
    await page.click('button:has-text("Above")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Merged")');
    await page.waitForTimeout(300);

    const triStyles = ['classic', 'offset', 'layers', 'corners', 'unequal'];
    for (const style of triStyles) {
        await page.selectOption('#styleSelect', style);
        await page.waitForTimeout(500);
        await page.click('button:has-text("Merged")');
        await page.waitForTimeout(300);
        await page.screenshot({ path: `tri-${style}-merged.png` });
        console.log(`Triangle ${style}: merged`);
    }

    // Test Pentagon styles
    console.log('--- PENTAGON ---');
    await page.click('button:has-text("Pentagon")');
    await page.waitForTimeout(500);
    const pentStyles = ['classic', 'offset', 'corners'];
    for (const style of pentStyles) {
        await page.selectOption('#styleSelect', style);
        await page.waitForTimeout(500);
        await page.click('button:has-text("Merged")');
        await page.waitForTimeout(300);
        await page.screenshot({ path: `pent-${style}-merged.png` });
        console.log(`Pentagon ${style}: merged`);
    }

    // Test Hexagon styles
    console.log('--- HEXAGON ---');
    await page.click('button:has-text("Hexagon")');
    await page.waitForTimeout(500);
    const hexStyles = ['classic', 'offset', 'corners'];
    for (const style of hexStyles) {
        await page.selectOption('#styleSelect', style);
        await page.waitForTimeout(500);
        await page.click('button:has-text("Merged")');
        await page.waitForTimeout(300);
        await page.screenshot({ path: `hex-${style}-merged.png` });
        console.log(`Hexagon ${style}: merged`);
    }

    await browser.close();
})();
