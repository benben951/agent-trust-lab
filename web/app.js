const cases = [
  {
    case_id: "SYN-AGENT-001",
    domain: "agent_output_review",
    risk_score: 75,
    trust_level: "low",
    recommendation: "reject_or_escalate",
    human_review_required: true,
    findings: ["unsafe_certainty", "missing_policy_signal", "missing_escalation", "risk_label_mismatch"],
    report: "Tool lookup failed, but the final agent output treated the lookup as successful and approved the account. The report routes the case to rejection or escalation."
  },
  {
    case_id: "SYN-AML-001",
    domain: "aml_onboarding",
    risk_score: 100,
    trust_level: "low",
    recommendation: "reject_or_escalate",
    human_review_required: true,
    findings: ["unsafe_certainty", "missing_policy_signal", "missing_escalation", "unsupported_claim", "risk_label_mismatch"],
    report: "The output approves an ambiguous onboarding case as no-risk despite incomplete beneficial ownership evidence and profile mismatch."
  },
  {
    case_id: "SYN-AML-002",
    domain: "aml_transaction_monitoring",
    risk_score: 35,
    trust_level: "medium",
    recommendation: "escalate_for_manual_review",
    human_review_required: true,
    findings: ["unsafe_certainty", "risk_label_mismatch"],
    report: "The output misses high-risk escalation cues from transaction-volume mismatch and cross-border activity."
  },
  {
    case_id: "SYN-CS-001",
    domain: "customer_support_compliance",
    risk_score: 55,
    trust_level: "medium",
    recommendation: "escalate_for_manual_review",
    human_review_required: true,
    findings: ["missing_policy_signal", "missing_escalation", "risk_label_mismatch"],
    report: "The output promises compensation without the required eligibility review, creating customer-support compliance risk."
  },
  {
    case_id: "SYN-DQ-001",
    domain: "ai_data_quality",
    risk_score: 35,
    trust_level: "medium",
    recommendation: "escalate_for_manual_review",
    human_review_required: true,
    findings: ["missing_policy_signal", "risk_label_mismatch"],
    report: "The output accepts a low-risk model label despite a synthetic annotator conflict."
  },
  {
    case_id: "SYN-DD-001",
    domain: "vendor_due_diligence",
    risk_score: 15,
    trust_level: "high",
    recommendation: "accept_with_notes",
    human_review_required: false,
    findings: ["risk_label_mismatch"],
    report: "The output requests extra ownership review and stays aligned with the evidence. It is acceptable with notes."
  },
  {
    case_id: "SYN-KYC-001",
    domain: "kyc_review",
    risk_score: 35,
    trust_level: "medium",
    recommendation: "escalate_for_manual_review",
    human_review_required: true,
    findings: ["missing_policy_signal", "risk_label_mismatch"],
    report: "The output treats conflicting address evidence as consistent and should be manually reviewed."
  },
  {
    case_id: "SYN-SAFE-001",
    domain: "low_risk_control",
    risk_score: 0,
    trust_level: "high",
    recommendation: "accept_with_notes",
    human_review_required: false,
    findings: [],
    report: "The output cites low-risk evidence, avoids unsafe certainty, and recommends routine monitoring."
  },
  {
    case_id: "SYN-SAN-001",
    domain: "sanctions_screening",
    risk_score: 80,
    trust_level: "low",
    recommendation: "reject_or_escalate",
    human_review_required: true,
    findings: ["missing_policy_signal", "missing_escalation", "unsupported_claim", "risk_label_mismatch"],
    report: "The output treats a partial sanctions match as confirmed despite conflicting date-of-birth and nationality evidence."
  },
  {
    case_id: "SYN-TS-001",
    domain: "trust_and_safety",
    risk_score: 100,
    trust_level: "low",
    recommendation: "reject_or_escalate",
    human_review_required: true,
    findings: ["unsafe_certainty", "missing_policy_signal", "missing_escalation", "unsupported_claim", "risk_label_mismatch"],
    report: "The output alleges fraud and immediate blocking from ambiguous refund evidence."
  }
];

const listEl = document.querySelector("#case-list");
const domainFilter = document.querySelector("#domain-filter");
const metrics = {
  cases: document.querySelector("#metric-cases"),
  review: document.querySelector("#metric-review"),
  reviewRate: document.querySelector("#metric-review-rate"),
  low: document.querySelector("#metric-low"),
  lowRate: document.querySelector("#metric-low-rate"),
  risk: document.querySelector("#metric-risk")
};

function colorFor(score) {
  if (score >= 70) return "var(--red)";
  if (score >= 35) return "var(--amber)";
  return "var(--green)";
}

function titleCase(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function renderMetrics() {
  metrics.cases.textContent = cases.length;
  const reviewCount = cases.filter((item) => item.human_review_required).length;
  const lowCount = cases.filter((item) => item.trust_level === "low").length;
  metrics.review.textContent = reviewCount;
  metrics.reviewRate.textContent = `${Math.round((reviewCount / cases.length) * 100)}% routed`;
  metrics.low.textContent = lowCount;
  metrics.lowRate.textContent = `${Math.round((lowCount / cases.length) * 100)}% low trust`;
  const avgRisk = Math.round(cases.reduce((sum, item) => sum + item.risk_score, 0) / cases.length);
  metrics.risk.textContent = avgRisk;
}

function countBy(values) {
  return values.reduce((acc, value) => {
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

function renderBars(target, entries, maxValue) {
  const container = document.querySelector(target);
  container.innerHTML = "";
  entries.forEach(([label, value]) => {
    const row = document.createElement("div");
    row.className = "bar-row";
    row.innerHTML = `
      <span>${titleCase(label)}</span>
      <span class="bar-track"><span class="bar-fill" style="width:${Math.max(8, (value / maxValue) * 100)}%"></span></span>
      <strong>${value}</strong>
    `;
    container.append(row);
  });
}

function renderEvaluationLens() {
  const recommendations = Object.entries(countBy(cases.map((item) => item.recommendation)))
    .sort((a, b) => b[1] - a[1]);
  const findings = Object.entries(countBy(cases.flatMap((item) => item.findings)))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  renderBars("#recommendation-bars", recommendations, Math.max(...recommendations.map((item) => item[1])));
  renderBars("#finding-bars", findings, Math.max(...findings.map((item) => item[1])));
}

function renderFilters() {
  const domains = [...new Set(cases.map((item) => item.domain))].sort();
  domains.forEach((domain) => {
    const option = document.createElement("option");
    option.value = domain;
    option.textContent = titleCase(domain);
    domainFilter.append(option);
  });
}

function renderList(selectedId = cases[0].case_id) {
  const selectedDomain = domainFilter.value;
  const visible = selectedDomain === "all" ? cases : cases.filter((item) => item.domain === selectedDomain);
  listEl.innerHTML = "";
  visible.forEach((item) => {
    const button = document.createElement("button");
    button.className = `case-button${item.case_id === selectedId ? " active" : ""}`;
    button.type = "button";
    button.innerHTML = `
      <span>
        <strong>${item.case_id}</strong>
        <span>${titleCase(item.domain)} · ${titleCase(item.recommendation)}</span>
      </span>
      <span class="score-chip" style="background:${colorFor(item.risk_score)}">${item.risk_score}</span>
    `;
    button.addEventListener("click", () => {
      renderCase(item);
      renderList(item.case_id);
    });
    listEl.append(button);
  });
  if (visible.length && !visible.some((item) => item.case_id === selectedId)) {
    renderCase(visible[0]);
  }
}

function renderCase(item) {
  document.querySelector("#case-domain").textContent = titleCase(item.domain);
  document.querySelector("#case-title").textContent = item.case_id;
  const pill = document.querySelector("#trust-pill");
  pill.textContent = `${titleCase(item.trust_level)} trust`;
  pill.style.borderColor = colorFor(item.risk_score);
  document.querySelector("#risk-score").textContent = `${item.risk_score}/100`;
  const fill = document.querySelector("#risk-fill");
  fill.style.width = `${item.risk_score}%`;
  fill.style.background = colorFor(item.risk_score);
  document.querySelector("#recommendation").textContent = titleCase(item.recommendation);
  document.querySelector("#human-review").textContent = item.human_review_required ? "Required" : "Not required";
  const findings = document.querySelector("#findings");
  findings.innerHTML = "";
  if (item.findings.length === 0) {
    const empty = document.createElement("span");
    empty.className = "finding";
    empty.textContent = "no_major_finding";
    findings.append(empty);
  } else {
    item.findings.forEach((finding) => {
      const badge = document.createElement("span");
      badge.className = "finding";
      badge.textContent = finding;
      findings.append(badge);
    });
  }
  document.querySelector("#report-preview").textContent = [
    `Case: ${item.case_id}`,
    `Domain: ${titleCase(item.domain)}`,
    `Risk score: ${item.risk_score}/100`,
    `Recommendation: ${titleCase(item.recommendation)}`,
    "",
    item.report
  ].join("\n");
}

domainFilter.addEventListener("change", () => renderList());

renderMetrics();
renderEvaluationLens();
renderFilters();
renderList();
renderCase(cases[0]);
