import datetime
import openai
import streamlit as st

# 获取终端输出并显示表格
def list_fine_tuned_tasks(api_key):
    openai.api_key = api_key
    terminal_output = openai.FineTune.list()
    return terminal_output["data"]

# 解析终端输出为表格行列表
def parse_terminal_output(terminal_output):
    rows = []
    for task in terminal_output:
        hyperparams = task["hyperparams"]
        training_file = task["training_files"][0]["filename"]

        created_at = datetime.datetime.fromtimestamp(task["created_at"]).strftime("%Y-%m-%d %H:%M:%S")

        row = {
            "Time": created_at,
            "Model Name": task["fine_tuned_model"],
            "Job ID": task["id"],
            "Parent Model": task["model"],
            "Status": task["status"],
            "Batch Size": hyperparams["batch_size"],
            "Learning Rate Multiplier": hyperparams["learning_rate_multiplier"],
            "Epochs": hyperparams["n_epochs"],
            "Prompt Loss Weight": hyperparams["prompt_loss_weight"],
            "Training File": training_file
        }
        rows.append(row)

    return rows

# 取消 Fine-Tune 任务
def cancel_fine_tune_job(api_key, job_id):
    openai.api_key = api_key
    try:
        openai.FineTune.retrieve(id=job_id)
    except openai.error.InvalidRequestError:
        return "invalid"
    else:
        response = openai.FineTune.cancel(id=job_id)
        return response["status"]

# 读取 API 密钥
api_key = st.text_input("Enter your OpenAI API key", type="password")

# 当用户提供 API 密钥时，获取终端输出并解析为表格行列表
if api_key:
    tasks = list_fine_tuned_tasks(api_key)
    rows = parse_terminal_output(tasks)
    st.table(rows)

    # 获取要取消的任务 ID
    job_id_to_cancel = st.text_input("Enter the Job ID to cancel")

    if st.button("Cancel Job"):
        if job_id_to_cancel:
            status = cancel_fine_tune_job(api_key, job_id_to_cancel)
            if status == "cancelled":
                st.success("The job is successfully canceled")
            elif status == "invalid":
                st.error("Invalid Job ID. Please enter a valid Job ID.")
            else:
                st.error("Failed to cancel the job")
        else:
            st.warning("Please enter a valid Job ID")
else:
    st.warning("Please enter your OpenAI API key.")
