# Road4AI Referral Program Implementation Status

This checklist tracks the implementation of the Road4AI referral program across strategy, copy, UI/CLI, GA4 tracking, and Stripe integration.

---

## 1. Strategy & Incentive Design
- [x] **Propose 3 distinct incentive structures**
  * **Evidence:** `referral_program_proposal.md#L7-L41`
  * **Note:** Done. Compute credits (A), Swag/Skills (B), and Recurring Commission (C) proposed.
- [ ] **Select and finalize the active incentive structure**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Needs decision by the user/owner.
- [ ] **Define program terms, conditions, and payout timelines**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Legal terms, abuse limits, and payout schedules are not yet drafted.

## 2. Copy & Communication
- [x] **Draft launch email copy in Sharon's brand voice**
  * **Evidence:** `referral_program_proposal.md#L44-L77`
  * **Note:** Done.
- [ ] **Draft reminder emails and nurture sequences for non-referrers**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Email sequences for reminder campaigns are not yet drafted.
- [ ] **Design in-app sharing prompts and CLI messages**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Exact copy for CLI terminal messages and sharing prompts is not yet defined.

## 3. Frontend & UI/CLI Development
- [ ] **Build the referral landing/signup page copy and layout**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Frontend signup page and landing template must be designed and coded.
- [ ] **Implement CLI endpoint `road4ai referral --link`**
  * **Evidence:** `referral_program_proposal.md#L62`
  * **Note:** The command is referenced in the email draft but needs to be added to the CLI tool.
- [ ] **Integrate user login state to generate unique referral links**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Database relationship must be established to map users to unique referral codes.

## 4. GA4 Tracking
- [x] **Write code to parse `ref` parameter from URL and store in `sessionStorage`**
  * **Evidence:** `referral_program_proposal.md#L88-L99`
  * **Note:** Done. Script code provided.
- [x] **Write code to trigger custom `signup_completed` event and set user properties**
  * **Evidence:** `referral_program_proposal.md#L101-L119`
  * **Note:** Done. Script code provided.
- [ ] **Add GA4 measurement script and test parameters in DebugView**
  * **Evidence:** `referral_program_proposal.md`
  * **Note:** Tracking code must be loaded into web pages and tested.
- [ ] **Register custom dimensions in GA4 Admin dashboard**
  * **Evidence:** `referral_program_proposal.md#L120-L125`
  * **Note:** Custom dimensions `referred_by_code` and `referral_code` need to be set up manually in the GA4 Console.

## 5. Stripe Tracking & Integration
- [ ] **Choose integration approach (Tolt/Rewardful vs Custom Metadata)**
  * **Evidence:** `referral_program_proposal.md#L128-L144`
  * **Note:** Decision required between third-party SaaS integrations or a zero-dependency custom codebase.
- [x] **Write Stripe Checkout Session metadata integration**
  * **Evidence:** `referral_program_proposal.md#L146-L172`
  * **Note:** Done. Integration code provided.
- [x] **Write webhook handler code for `invoice.payment_succeeded` events**
  * **Evidence:** `referral_program_proposal.md#L174-L208`
  * **Note:** Done. Webhook handler code provided.
- [ ] **Implement backend credit-applying logic `applyReferralCredit`**
  * **Evidence:** `referral_program_proposal.md#L201`
  * **Note:** Function mapping referral code to backend credits ledger and user account database is not yet coded.
- [ ] **Set up production webhooks and secure signature verification**
  * **Evidence:** `referral_program_proposal.md#L184`
  * **Note:** Production Stripe webhook endpoint and secrets must be configured.
