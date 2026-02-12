/*
 * Copyright (c) LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
 * See LICENSE in the project root for license information.
 */

package com.linkedin.flashback;

import com.linkedin.restli.server.annotations.RestLiActions;
import com.linkedin.restli.server.annotations.ActionParam;
import com.linkedin.restli.server.annotations.Optional;

/**
 * Health check resource for service monitoring.
 */
@RestLiActions(name = "health", namespace = "com.linkedin.flashback")
public class HealthResource {

  private static final String HEALTHY = "OK";

  @com.linkedin.restli.server.annotations.Action(name = "check")
  public String check(@ActionParam("status") @Optional String status) {
    return HEALTHY;
  }
}