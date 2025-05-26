from mcp.server.fastmcp import FastMCP
from typing import List
from datetime import date

# In-memory employee leave data store
employee_leaves = {
    "E001": {
        "balance": 20,
        "history": [
            {
                "date": "2024-12-25",
                "reason": "Christmas",
                "type": "casual",
                "status": "approved",
                "applied_on": "2024-12-20"
            }
        ]
    },
    "E002": {
        "balance": 15,
        "history": []
    }
}

# Initialize MCP server
mcp = FastMCP("LeaveManagementSystem")

# Tool: Apply for leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str], reason: str, leave_type: str) -> str:
    """
    Apply for leave with dates, reason, and type.
    Example:
    - leave_dates = ["2025-05-10", "2025-05-11"]
    - reason = "Family function"
    - leave_type = "casual"
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    balance = employee_leaves[employee_id]["balance"]

    if balance < requested_days:
        return f"Insufficient leave balance. Requested {requested_days}, available {balance}."

    # Apply leave
    for dt in leave_dates:
        employee_leaves[employee_id]["history"].append({
            "date": dt,
            "reason": reason,
            "type": leave_type,
            "status": "pending",  # Default to pending
            "applied_on": str(date.today())
        })

    employee_leaves[employee_id]["balance"] -= requested_days
    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

# Tool: Check leave balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check current leave balance for an employee."""
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    return f"{employee_id} has {employee_leaves[employee_id]['balance']} leave days remaining."

# Tool: View leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> List[dict]:
    """Get detailed leave history for an employee."""
    if employee_id not in employee_leaves:
        return []
    return employee_leaves[employee_id]["history"]

# Resource: Personalized greeting
@mcp.resource("greeting://{name}")
def greet_user(name: str) -> str:
    """Greeting for leave management system"""
    return f"Hello, {name}! Welcome to the Leave Management System."

# Start the MCP server
if __name__ == "__main__":
    mcp.run()
