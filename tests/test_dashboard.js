// Regression tests for time rendering and HTML escaping in the shipped dashboard.
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const file = path.join(__dirname, '..', 'pet_bathroom_tracker', 'templates', 'index.html');
const html = fs.readFileSync(file, 'utf8');
function readOneLineDeclaration(name) {
  const match = html.match(new RegExp('^const ' + name + '=.*;$', 'm'));
  assert.ok(match, `${name} declaration missing or no longer a single line`);
  return vm.runInNewContext('(() => { ' + match[0] + '; return ' + name + '; })()');
}
const timeOf = readOneLineDeclaration('timeOf');
const esc = readOneLineDeclaration('esc');

// Saved timestamps are local wall-clock values and should never be normalized
// through a browser timezone or daylight-saving-time transition.
assert.equal(timeOf('2026-03-08T02:30:00'), '2:30 AM');
assert.equal(timeOf('2026-11-01T01:30:00'), '1:30 AM');
assert.equal(timeOf('2026-04-01T00:05:00'), '12:05 AM');
assert.equal(timeOf('2026-04-01T12:00:00'), '12:00 PM');
assert.equal(timeOf('2026-04-01T23:59:00'), '11:59 PM');
assert.equal(esc('<img src=x onerror="alert(1)">'), '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');
assert.equal(esc("<script>alert('x')</script>"), '&lt;script&gt;alert(&#39;x&#39;)&lt;/script&gt;');
console.log('Dashboard time formatting and HTML escaping tests passed');
