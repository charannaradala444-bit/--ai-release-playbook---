import streamlit as st
import datetime

class ResponsibleReleaseTool:
    def __init__(self, project_name):
        self.project_name = project_name
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results = {}
        self.failed_items = []

        self.checklist = {
            "PHASE A: ETHICS & BIAS": [
                ("E1", "Has the model passed the Demographic Parity (Fairness) test?"),
                ("E2", "Have all toxicity and stereotype filters been verified?"),
                ("E3", "Is the UI accessible for disabled users (WCAG Compliant)?")
            ],
            "PHASE B: DATA & PRIVACY": [
                ("D1", "Is all PII (names/phones) encrypted or hashed?"),
                ("D2", "Do we have documented legal consent for all data used?"),
                ("D3", "Has the data lineage been verified (Source of Truth)?")
            ],
            "PHASE C: GOVERNANCE": [
                ("G1", "Has the designated Human Owner signed off?"),
                ("G2", "Is the 'Rollback Plan' tested and ready?"),
                ("G3", "Did the system pass the Security Red-Team attack?")
            ]
        }

    def run_checklist(self):
        st.title(f"🛡️ Responsible Release Playbook - {self.project_name}")
        st.write(f"**Date:** {self.timestamp}")
        st.write("### Instructions")
        st.write("Run your external tests first. Then answer each question below:")

        for phase, items in self.checklist.items():
            st.subheader(phase)
            phase_passed = True

            for check_id, question in items:
                response = st.radio(f"[{check_id}] {question}", ["Yes", "No"], key=check_id)
                if response == "Yes":
                    self.results[check_id] = "PASS"
                else:
                    self.results[check_id] = "FAIL"
                    self.failed_items.append(f"{phase} -> {check_id}: {question}")
                    phase_passed = False

            if not phase_passed:
                st.error(f"❌ CRITICAL FAILURE IN {phase}. STOPPING REVIEW.")
                break
            else:
                st.success(f"{phase} Passed.")

        self.generate_report()

    def generate_report(self):
        st.write("## 📝 Final Decision Report")
        if len(self.failed_items) == 0:
            st.success("✅ RESULT: GO - LAUNCH APPROVED")
            st.write("All governance checks have been verified successfully.")
        else:
            st.error("🚫 RESULT: NO-GO - RELEASE BLOCKED")
            st.write("The following checks failed and must be fixed:")
            for item in self.failed_items:
                st.warning(f"⚠ {item}")
            st.write("**Action:** Return software to Development Phase.")

# --- Streamlit App ---
if __name__ == "__main__":
    tool = ResponsibleReleaseTool("MediScan")
    tool.run_checklist()