#!/bin/bash

# Test script for Django Messaging App Kubernetes deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Test 1: Check if deployment exists
test_deployment_exists() {
    print_status "Checking if deployment exists..."
    if kubectl get deployment messaging-app-deployment &> /dev/null; then
        print_success "Deployment exists"
        return 0
    else
        print_error "Deployment not found"
        return 1
    fi
}

# Test 2: Check if pods are running
test_pods_running() {
    print_status "Checking if pods are running..."
    RUNNING_PODS=$(kubectl get pods -l app=messaging-app --field-selector=status.phase=Running --no-headers | wc -l)
    if [ "$RUNNING_PODS" -gt 0 ]; then
        print_success "$RUNNING_PODS pods are running"
        return 0
    else
        print_error "No pods are running"
        return 1
    fi
}

# Test 3: Check if service exists
test_service_exists() {
    print_status "Checking if service exists..."
    if kubectl get service messaging-app-service &> /dev/null; then
        print_success "Service exists"
        return 0
    else
        print_error "Service not found"
        return 1
    fi
}

# Test 4: Check logs for errors
test_pod_logs() {
    print_status "Checking pod logs for errors..."
    LOGS=$(kubectl logs -l app=messaging-app --tail=50 2>/dev/null || echo "")
    
    if echo "$LOGS" | grep -i "error\|exception\|traceback" &> /dev/null; then
        print_error "Errors found in pod logs"
        echo "Recent log entries:"
        echo "$LOGS" | tail -10
        return 1
    else
        print_success "No errors in pod logs"
        return 0
    fi
}

# Test 5: Check if application responds
test_app_response() {
    print_status "Testing application response..."
    
    # Start port forwarding in background
    kubectl port-forward service/messaging-app-service 8000:8000 &
    PID=$!
    
    # Wait for port forwarding to be ready
    sleep 5
    
    # Test if app responds
    if curl -s http://localhost:8000/api/ &> /dev/null; then
        print_success "Application responds to HTTP requests"
        RESULT=0
    else
        print_error "Application does not respond"
        RESULT=1
    fi
    
    # Clean up port forwarding
    kill $PID 2>/dev/null || true
    
    return $RESULT
}

# Run all tests
main() {
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  Django Messaging App - Deployment Test   ${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    
    TOTAL_TESTS=5
    PASSED_TESTS=0
    
    # Run tests
    if test_deployment_exists; then ((PASSED_TESTS++)); fi
    echo ""
    
    if test_pods_running; then ((PASSED_TESTS++)); fi
    echo ""
    
    if test_service_exists; then ((PASSED_TESTS++)); fi
    echo ""
    
    if test_pod_logs; then ((PASSED_TESTS++)); fi
    echo ""
    
    if test_app_response; then ((PASSED_TESTS++)); fi
    echo ""
    
    # Summary
    echo -e "${BLUE}Test Summary:${NC}"
    echo "Passed: $PASSED_TESTS/$TOTAL_TESTS"
    
    if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
        print_success "All tests passed! Deployment is working correctly."
        exit 0
    else
        print_error "Some tests failed. Check the deployment."
        exit 1
    fi
}

main "$@"
