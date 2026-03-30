import pytest
from unittest.mock import MagicMock, patch
from app.services.edge_manager import EdgeManager

@pytest.fixture
def mock_edge_manager():
    return EdgeManager(host="1.2.3.4", user="testuser", key_path="/path/to/key")

def test_check_gpu_status_active(mock_edge_manager, mocker):
    # Mock execute_command
    mocker.patch.object(
        mock_edge_manager, 
        'execute_command', 
        return_value=(0, "NVIDIA A100-SXM4-40GB, 470.57.02, 40536 MiB", "")
    )
    
    status = mock_edge_manager.check_gpu_status()
    
    assert status["status"] == "active"
    assert status["gpu_name"] == "NVIDIA A100-SXM4-40GB"
    assert status["driver_version"] == "470.57.02"
    assert status["memory_total"] == "40536 MiB"

def test_check_gpu_status_inactive(mock_edge_manager, mocker):
    # Mock execute_command failure
    mocker.patch.object(
        mock_edge_manager, 
        'execute_command', 
        return_value=(1, "", "nvidia-smi: command not found")
    )
    
    status = mock_edge_manager.check_gpu_status()
    
    assert status["status"] == "inactive"
    assert "error" in status

def test_get_vm_status_running(mock_edge_manager, mocker):
    mocker.patch.object(
        mock_edge_manager, 
        'execute_command', 
        return_value=(0, "running", "")
    )
    
    status = mock_edge_manager.get_vm_status("test-vm")
    assert status == "running"

def test_start_vm_success(mock_edge_manager, mocker):
    mock_exec = mocker.patch.object(
        mock_edge_manager, 
        'execute_command', 
        return_value=(0, "Domain test-vm started", "")
    )
    
    result = mock_edge_manager.start_vm("test-vm")
    
    assert result is True
    mock_exec.assert_called_with("sudo virsh start test-vm")

def test_stop_vm_failure(mock_edge_manager, mocker):
    mocker.patch.object(
        mock_edge_manager, 
        'execute_command', 
        return_value=(1, "", "error: failed to get domain 'test-vm'")
    )
    
    result = mock_edge_manager.stop_vm("test-vm")
    assert result is False

@patch("paramiko.SSHClient")
def test_ssh_connection_context_manager(mock_ssh_client_class, mock_edge_manager):
    # Mock behavior of SSHClient
    mock_client = mock_ssh_client_class.return_value
    
    with mock_edge_manager.ssh_connection() as client:
        assert client == mock_client
        mock_client.connect.assert_called_once()
    
    mock_client.close.assert_called_once()
