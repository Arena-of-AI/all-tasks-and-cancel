import streamlit as st
import openai
from datetime import datetime

# 设置 OpenAI API 密钥输入框
api_key = st.text_input("Enter your OpenAI API key")

# 初始化 OpenAI
openai.api_key = api_key

# 列出所有 FineTune 作业
def list_all_jobs():
    try:
        response = openai.FineTune.list()
        data = response["data"]

        table_data = []
        for item in data:
            created_at = datetime.fromtimestamp(item["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
            fine_tuned_model = item["fine_tuned_model"]
            model = item["model"]
            status = item["status"]
            table_data.append((created_at, fine_tuned_model, model, status))

        st.table(table_data, headers=["Created At", "Fine-Tuned Model", "Model", "Status"])
    except openai.error.AuthenticationError as e:
        st.error(str(e))

# 取消 FineTune 作业
def cancel_job(job_id):
    try:
        response = openai.FineTune.cancel(id=job_id)
        status = response["status"]
        if status == "cancelled":
            st.success("The job is successfully canceled.")
        else:
            st.error("Failed to cancel the job.")
    except openai.error.AuthenticationError as e:
        st.error(str(e))

# 主应用
def main():
    st.title("OpenAI Fine-Tune Jobs")

    # 显示列表按钮
    if st.button("List All Jobs"):
        list_all_jobs()

    # 取消作业输入框和按钮
    cancel_job_id = st.text_input("Enter the Job ID to cancel")
    if st.button("Cancel Job") and cancel_job_id:
        cancel_job(cancel_job_id)

# 运行主应用
if __name__ == "__main__":
    main()
