import json,uuid
from evidently.report import Report
from evidently.metric_preset import TargetDriftPreset,DataDriftPreset
from .utility.constants import DataConnector, DriftType, ProblemType
from evidently.pipeline.column_mapping import ColumnMapping
from .utility.datasource import DataSource
from .utility.drift_util import get_alert_configurations, clean_drift_configurations
from .utility.constants import AlertParams
from .utility.drift_util import generate_alerts,save_drifts_and_alerts

def execute_drift(session, drift_type,drift_configurations):
    # read datasets for drift execution
    try:
        datasource = DataSource(session, drift_configurations, DataConnector.SNOWFLAKE)
        sf_current, sf_reference = datasource.load_snowflake_datasets()
    except Exception as msg:
        return False, f"Error in loading datasets : {msg}"

    ## column names corrections in drift configurations
    drift_configurations = clean_drift_configurations(drift_configurations,sf_reference)

    ## drift_score alert configurations
    alert_configurations = drift_configurations["alerts_configurations"] if "alerts_configurations" in drift_configurations else None

    if drift_type == DriftType.FEATURE_DRIFT:
        try:
            column_mapping = ColumnMapping()

            # prepare pandas datasets for feature drift
            current, reference = sf_current.to_pandas(), sf_reference.to_pandas()
            feature_columns = drift_configurations["feature_columns"]
            current = current[feature_columns]
            reference = reference[feature_columns]

            feature_drift_obj = DataDriftPreset()
            data_drift_report = Report(metrics=[feature_drift_obj])
            data_drift_report.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
            feature_drift_report_data = json.loads(data_drift_report.json())
            
            ## Alert generations
            feature_drift_configs = get_alert_configurations(alert_configurations,AlertParams.DRIFT_SCORE)
            alerts_data,metric_info = generate_alerts(feature_drift_report_data,feature_drift_configs,drift_type)

            feature_drift_report_data['metric_info'] = metric_info
            feature_drift_id = str(uuid.uuid4()) 

            ## Save the reports for Alerts & Drifts
            save_drifts_and_alerts(session,
                                feature_drift_report_data,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                feature_drift_id)
            
        except Exception as msg:
            return False, f"Error in feature drift execution : {msg}"
    
        return True,"Feature Drift recipe executed successfully !!"
        
    elif drift_type in [DriftType.LABEL_DRIFT,DriftType.PREDICTION_DRIFT]:
        try:
            column_mapping = ColumnMapping() ; recipe_name = None ; target_column = None
            current, reference = sf_current.to_pandas(), sf_reference.to_pandas()

            if drift_type == DriftType.LABEL_DRIFT:
                column_mapping.prediction = 'None'
                column_mapping.target = drift_configurations['target_column']
                target_column = drift_configurations['target_column']
                recipe_name = "Label Drift"
            else:
                column_mapping.prediction = drift_configurations['prediction_column']
                column_mapping.target = 'None'
                target_column = drift_configurations['prediction_column']
                recipe_name = "Prediction Drift"

            # Drift execution
            drift_report = Report(metrics=[TargetDriftPreset()])
            drift_report.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
            drift_report_ouput = json.loads(drift_report.json())

            ## Plots
            is_numerical = True
            try:
                current[target_column].astype(int)
                if len(current[target_column].unique()) < 50:
                    is_numerical = False
            except:
                is_numerical = False

            if not is_numerical:
                histogram_plots = {}
                histogram_plots['current'] = current[target_column].value_counts().sort_index().to_dict()
                histogram_plots['reference'] = reference[target_column].value_counts().sort_index().to_dict()
                drift_report_ouput["metrics"].append({
                    "metric" : "histogram_plot",
                    "result" : histogram_plots
                })
            else:
                total_rows = len(current)
                interval = total_rows // 140
                current_rows = current.iloc[::interval] if interval > 0 else current
                reference_rows = reference.iloc[::interval] if interval > 0 else reference

                sample_records = {}
                sample_records['current'] = {"index_numbers":list(current_rows[target_column].to_dict().keys()),
                                                    "values":list(current_rows[target_column].to_dict().values())}
                sample_records['reference'] = {"index_numbers":list(reference_rows[target_column].to_dict().keys()),
                                                      "values":list(reference_rows[target_column].to_dict().values())}
                drift_report_ouput["metrics"].append({
                    "metric" : "sample_records",
                    "result" : sample_records
                })
            
            # Alert generations
            label_drift_configs = get_alert_configurations(alert_configurations,AlertParams.DRIFT_SCORE)
            alerts_data,metric_info = generate_alerts(drift_report_ouput,label_drift_configs,drift_type)

            drift_report_ouput['metric_info'] = metric_info
            drift_id = str(uuid.uuid4())

            # Save the reports for Alerts & Drifts
            save_drifts_and_alerts(session,
                                drift_report_ouput,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                drift_id)
        except Exception as msg:
            # raise Exception(f"Error in label drift execution : {msg}")
            return False, f"error in {drift_type} execution : {msg}"

        return True,f"{recipe_name} recipe executed successfully !!"

    elif drift_type == DriftType.MODEL_PERFORMANCE_DRIFT:
        if drift_configurations['problem_type'] == ProblemType.CLASSIFICATION:
            from .utility.performance_drift import execute_classification_drift
            try:
                # drift execution
                drift_output = execute_classification_drift(
                    session,
                    drift_configurations,
                    sf_current,
                    sf_reference)
                
                # alert generations
                performance_alert_configs = get_alert_configurations(alert_configurations,AlertParams.PERFORMANCE_DRIFT_SCORE)
                alert_data, metric_info = generate_alerts(drift_output,performance_alert_configs,drift_type,ProblemType.CLASSIFICATION)
            
                drift_output['metric_info'] = metric_info
                drift_id = str(uuid.uuid4())
                
                # saving the reports for Alerts & Drifts
                save_drifts_and_alerts(session,
                                drift_output,
                                alert_data,
                                drift_configurations,
                                drift_type,
                                drift_id)
            except Exception as msg:
                return False, f"Error in model performance drift execution : {msg}"
            
        elif drift_configurations['problem_type'] == ProblemType.REGRESSION:
            from .utility.performance_drift import execute_regression_drift
            try:
                # drift execution
                drift_output = execute_regression_drift(drift_configurations,sf_current,sf_reference)

                # alert generations
                performance_alert_configs = get_alert_configurations(alert_configurations,AlertParams.PERFORMANCE_DRIFT_SCORE)
                alerts_data,metric_info = generate_alerts(drift_output,performance_alert_configs,drift_type,ProblemType.REGRESSION)

                drift_output['metric_info'] = metric_info
                drift_id = str(uuid.uuid4())

                # saving the reports for Alerts & Drifts
                save_drifts_and_alerts(session,
                                drift_output,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                drift_id)
                

            except Exception as msg:
                return False, f"Error in model performance drift execution : {msg}"
        else:
            return False, "Invalid problem type provided"
        
        return True,"Model Performance Drift recipe executed successfully !! "
    
    else:
        return False, "invalid drift type provided"
