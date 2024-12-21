import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_analytics(data_manager) -> None:
    st.title("📈 Financial Analytics")
    
    operations = data_manager.get_operations()
    if operations:
        df = pd.DataFrame(operations)
        df['date'] = pd.to_datetime(df['date'])
        
        tab1, tab2, tab3 = st.tabs(["Category Analysis", "Time Analysis", "Trends"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Expenses by Category")
                expenses = df[df['type'] == 'expense']
                category_sum = expenses.groupby('category')['amount'].sum().reset_index()
                fig = px.pie(
                    category_sum,
                    values='amount',
                    names='category',
                    title='Expense Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Category Breakdown")
                st.dataframe(
                    category_sum,
                    column_config={
                        "category": "Category",
                        "amount": st.column_config.NumberColumn(
                            "Amount",
                            format="$%.2f"
                        )
                    },
                    hide_index=True
                )
        
        with tab2:
            st.subheader("Monthly Trends")
            df['month'] = df['date'].dt.strftime('%Y-%m')
            monthly_data = df.pivot_table(
                index='month',
                columns='type',
                values='amount',
                aggfunc='sum'
            ).fillna(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_data.index,
                y=monthly_data['expense'],
                name='Expenses',
                marker_color='red'
            ))
            fig.add_trace(go.Bar(
                x=monthly_data.index,
                y=monthly_data['income'],
                name='Income',
                marker_color='green'
            ))
            fig.update_layout(barmode='group', title='Monthly Income vs Expenses')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Balance Trend")
            df_sorted = df.sort_values('date')
            df_sorted['cumulative_balance'] = df_sorted.apply(
                lambda x: x['amount'] if x['type'] == 'income' else -x['amount'],
                axis=1
            ).cumsum()
            
            fig = px.line(
                df_sorted,
                x='date',
                y='cumulative_balance',
                title='Balance Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for analysis. Add some transactions first!")